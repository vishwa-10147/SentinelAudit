"""
Sentinel Detection Engine
------------------------
Performs packet capture (pcap or live), flow extraction, anomaly detection (IsolationForest), risk scoring, MITRE ATT&CK mapping, and outputs results as JSON.

Modules:
- Flow: Represents a network flow.
- FlowExtractor: Aggregates packets into flows.
- FeatureBuilder: Converts flows to ML features.
- AnomalyDetector: Detects anomalies using IsolationForest.
- MitreMapper: Maps flows to MITRE ATT&CK techniques.
- AlertManager: Handles alerting (console/email).
- process_packets: Main detection pipeline.
- CLI: Command-line interface for running detection.
"""

from __future__ import annotations

import argparse
import json
import yaml
import logging
import os
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

try:
    from scapy.all import sniff, rdpcap, Packet
except Exception:  # pragma: no cover - informative import
    sniff = None  # type: ignore
    rdpcap = None  # type: ignore
    Packet = object  # type: ignore

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from joblib import dump, load as joblib_load
import smtplib
from email.message import EmailMessage
import sys
from sentinel.web.db_logger import log_detection

# Minimal AlertManager implementation for alerting
class AlertManager:
    def __init__(self, smtp_server=None, smtp_port=587, smtp_user=None, smtp_password=None, email_from=None, email_to=None):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.email_from = email_from
        self.email_to = email_to

    def alert_console(self, alert: dict) -> None:
        print(f"[ALERT] {alert.get('id', '')}: {alert.get('name', '')} | Confidence: {alert.get('confidence', 0)} | Reason: {alert.get('reason', '')}")

    def alert_email(self, alert: dict) -> None:
        if not (self.smtp_server and self.email_from and self.email_to):
            return
        msg = EmailMessage()
        msg['Subject'] = f"Sentinel Alert: {alert.get('id', '')} - {alert.get('name', '')}"
        msg['From'] = self.email_from
        msg['To'] = self.email_to
        msg.set_content(f"Alert: {alert.get('name', '')}\nConfidence: {alert.get('confidence', 0)}\nReason: {alert.get('reason', '')}")
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                if self.smtp_user and self.smtp_password:
                    server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
        except Exception as e:
            print(f"[ALERT EMAIL ERROR] {e}")

logger = logging.getLogger("sentinel.sniffer")
logging.basicConfig(level=logging.INFO)


@dataclass
class Flow:
    """Simple representation of a network flow between endpoints.

    Attributes:
        src_ip (str): Source IP address.
        src_port (Any): Source port.
        dst_ip (str): Destination IP address.
        dst_port (Any): Destination port.
        protocol (str): Protocol name (TCP/UDP/etc).
        start_time (float): Flow start timestamp.
        end_time (float): Flow end timestamp.
        packet_count (int): Number of packets in flow.
        byte_count (int): Total bytes in flow.
    """

    src_ip: str
    src_port: Any
    dst_ip: str
    dst_port: Any
    protocol: str
    start_time: float
    end_time: float
    packet_count: int
    byte_count: int

    def duration(self) -> float:
        """Return flow duration in seconds."""

        return max(0.0, self.end_time - self.start_time)


class FlowExtractor:
    """Extracts flows from scapy Packet objects.

    Methods:
        add_packet(pkt): Add a single packet to flow aggregation.
        add_packets(packets): Add multiple packets.
        flows(): Return list of aggregated flows.
    """

    def __init__(self) -> None:
        self._flows: Dict[Tuple[str, Any, str, Any, str], Flow] = {}

    def _key_from_pkt(self, pkt: Any) -> Any:
        """Create a flow key from a scapy packet.

        Returns None when packet doesn't contain IP layer.
        """

        try:
            ip_layer = pkt.getlayer("IP")
            if ip_layer is None:
                return None
            src = ip_layer.src
            dst = ip_layer.dst
            proto = ip_layer.proto
        except Exception:
            return None

        sport = None
        dport = None
        proto_name = str(proto)
        try:
            tcp = pkt.getlayer("TCP")
            if tcp is not None:
                sport = int(tcp.sport)
                dport = int(tcp.dport)
                proto_name = "TCP"
        except Exception:
            pass
        try:
            udp = pkt.getlayer("UDP")
            if udp is not None:
                sport = int(udp.sport)
                dport = int(udp.dport)
                proto_name = "UDP"
        except Exception:
            pass

        return (src, sport, dst, dport, proto_name)

    def add_packet(self, pkt: Any) -> None:
        """Add a single packet to flow aggregation."""

        key = self._key_from_pkt(pkt)
        if key is None:
            return

        ts = float(pkt.time) if hasattr(pkt, "time") else datetime.now().timestamp()
        length = len(pkt) if hasattr(pkt, "__len__") else 0

        if key in self._flows:
            f = self._flows[key]
            f.end_time = max(f.end_time, ts)
            f.packet_count += 1
            f.byte_count += length
        else:
            src, sport, dst, dport, proto = key
            self._flows[key] = Flow(
                src_ip=src,
                src_port=sport,
                dst_ip=dst,
                dst_port=dport,
                protocol=proto,
                start_time=ts,
                end_time=ts,
                packet_count=1,
                byte_count=length,
            )

    def add_packets(self, packets: list) -> None:
        """Add many packets at once."""

        for pkt in packets:
            self.add_packet(pkt)

    def flows(self) -> list:
        """Return list of aggregated flows."""

        return list(self._flows.values())


class FeatureBuilder:
    """Builds a pandas DataFrame of numeric features from Flow objects.

    Methods:
        build(flows): Convert flows to a feature DataFrame for ML.
    """

    feature_columns = ["packet_count", "byte_count", "duration", "avg_pkt_size"]

    @classmethod
    def build(cls, flows: list) -> Any:
        """Convert flows to a feature DataFrame suitable for ML.

        Columns: packet_count, byte_count, duration, avg_pkt_size
        """

        rows = []
        for f in flows:
            duration = f.duration()
            avg_pkt = f.byte_count / f.packet_count if f.packet_count > 0 else 0
            rows.append(
                {
                    "packet_count": f.packet_count,
                    "byte_count": f.byte_count,
                    "duration": duration,
                    "avg_pkt_size": avg_pkt,
                }
            )

        df = pd.DataFrame(rows)
        if df.empty:
            # provide a 0-row DataFrame with expected columns
            return pd.DataFrame(columns=cls.feature_columns)

        # simple normalization to make detection more stable
        df = df.fillna(0.0).astype(float)
        return df[cls.feature_columns]


class AnomalyDetector:
    """IsolationForest-based anomaly detector and risk scorer.

    Methods:
        fit(X): Fit the model.
        predict(X): Predict anomalies.
        anomaly_score(X): Score anomalies.
        save(path): Save model.
        load(path): Load model.
    """

    def __init__(self, seed: int = 42, contamination: float = 0.02) -> None:
        self.model = IsolationForest(random_state=seed, contamination=contamination)
        self._fitted = False

    def fit(self, X: Any) -> None:
        """Fit the IsolationForest model on feature matrix X."""

        if X.empty:
            self._fitted = False
            return
        self.model.fit(X.values)
        self._fitted = True

    def predict(self, X: Any) -> Any:
        """Return boolean array where True indicates anomaly."""

        if not self._fitted or X.empty:
            return np.array([False] * len(X))
        preds = self.model.predict(X.values)
        # sklearn returns -1 for anomaly, 1 for normal
        return preds == -1

    def anomaly_score(self, X: Any) -> Any:
        """Return anomaly scores in range [0, 1] where 1 is most anomalous."""

        if not self._fitted or X.empty:
            return np.zeros(len(X))
        # decision_function gives higher for normal; invert and scale
        raw = -self.model.decision_function(X.values)
        # min-max scale
        minv, maxv = float(np.min(raw)), float(np.max(raw))
        if maxv - minv <= 1e-9:
            return np.clip(raw / (maxv + 1e-9), 0.0, 1.0)
        return ((raw - minv) / (maxv - minv)).astype(float)

    def save(self, path: str) -> None:
        """Persist the underlying IsolationForest model to disk using joblib."""

        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        dump(self.model, path)

    @classmethod
    def load(cls, path: str) -> "AnomalyDetector":
        """Load a persisted IsolationForest model and return an AnomalyDetector wrapper."""

        if not os.path.exists(path):
            raise FileNotFoundError(f"Model file not found: {path}")
        model = joblib_load(path)
        inst = cls()
        inst.model = model
        inst._fitted = True
        return inst


class MitreMapper:
    """Map flows to MITRE ATT&CK techniques using YAML rules.

    Methods:
        map(flow, features, is_anomaly): Return list of ATT&CK techniques.
    """

    _rules = None
    _rules_path = os.path.join(os.path.dirname(__file__), "mitre_rules.yaml")

    @classmethod
    def _load_rules(cls):
        if cls._rules is not None:
            return cls._rules
        with open(cls._rules_path, "r", encoding="utf-8") as f:
            cls._rules = yaml.safe_load(f)
        return cls._rules

    @staticmethod
    def _eval_condition(val, cond):
        # cond can be a value, a list, or a string with operator
        if isinstance(cond, list):
            return val in cond
        if isinstance(cond, str):
            if cond.startswith(">="):
                return val >= float(cond[2:])
            if cond.startswith("<="):
                return val <= float(cond[2:])
            if cond.startswith(">"):
                return val > float(cond[1:])
            if cond.startswith("<"):
                return val < float(cond[1:])
            if cond.startswith("not_"):
                # e.g. not_dst_port: [80,443]
                return val not in cond[4:]
            # fallback: equality
            try:
                return val == type(val)(cond)
            except Exception:
                return False
        return val == cond

    @classmethod
    def map(cls, flow: Flow, features: Dict[str, float], is_anomaly: bool) -> List[Dict[str, str]]:
        """Return a list of possible ATT&CK techniques (id, name, confidence, reason) using YAML rules."""
        if not is_anomaly:
            return []
        rules = cls._load_rules()
        matches = []
        for rule in rules:
            match = rule.get("match", {})
            if not match:
                continue
            # Evaluate AND of all top-level match keys (except 'or' and 'not_')
            ok = True
            for k, v in match.items():
                if k == "or":
                    # OR of subconditions
                    or_ok = False
                    for sub in v:
                        for subk, subv in sub.items():
                            val = features.get(subk, getattr(flow, subk, None))
                            if val is not None and cls._eval_condition(val, subv):
                                or_ok = True
                    if not or_ok:
                        ok = False
                        break
                elif k.startswith("not_"):
                    field = k[4:]
                    val = features.get(field, getattr(flow, field, None))
                    if val is not None and cls._eval_condition(val, v):
                        ok = False
                        break
                else:
                    val = features.get(k, getattr(flow, k, None))
                    if val is None or not cls._eval_condition(val, v):
                        ok = False
                        break
            if ok:
                matches.append({
                    "id": rule["id"],
                    "name": rule["name"],
                    "confidence": rule["confidence"],
                    "reason": rule["reason"]
                })
        # If no match, use fallback (last rule)
        if not matches and rules:
            fallback = rules[-1]
            matches.append({
                "id": fallback["id"],
                "name": fallback["name"],
                "confidence": fallback["confidence"],
                "reason": fallback["reason"]
            })
        return matches


def process_packets(packets: list, detector: Any = None, alert_manager: Any = None) -> dict:
    """Process a list of scapy packets and return JSON-serializable results.

    Args:
        packets (list): List of scapy packets.
        detector (AnomalyDetector, optional): Anomaly detector instance.
        alert_manager (AlertManager, optional): Alert manager instance.

    Returns:
        dict: Results with flows, features, anomalies, risk scores, and MITRE mappings.
    """

    extractor = FlowExtractor()
    extractor.add_packets(packets)
    flows = extractor.flows()

    df = FeatureBuilder.build(flows)

    local_detector = detector if detector is not None else AnomalyDetector()
    if detector is None:
        # Only fit when we created the detector locally
        local_detector.fit(df)

    anomalies = local_detector.predict(df)
    scores = local_detector.anomaly_score(df)

    results = []
    for idx, flow in enumerate(flows):
        feats = df.iloc[idx].to_dict() if idx < len(df) else {}
        is_anom = bool(anomalies[idx]) if idx < len(anomalies) else False
        score = float(scores[idx]) if idx < len(scores) else 0.0
        mitre = MitreMapper.map(flow, feats, is_anom)

        # Alerting logic
        if alert_manager and mitre:
            for alert in mitre:
                alert_manager.alert_console(alert)
                if float(alert.get('confidence', 0)) >= 0.8:
                    alert_manager.alert_email(alert)

        # Log to dashboard DB if any MITRE mapping
        if mitre:
            log_detection(asdict(flow), mitre, int(round(score * 100)))

        results.append(
            {
                "flow": asdict(flow),
                "features": feats,
                "is_anomaly": is_anom,
                "risk_score": int(round(score * 100)),
                "mitre": mitre,
            }
        )

    return {"generated_at": datetime.now(timezone.utc).isoformat(), "results": results}


def read_pcap(path: str) -> list:
    """Read packets from a pcap file using scapy."""

    if rdpcap is None:
        raise RuntimeError("scapy is required to read pcap files; pip install scapy")
    return rdpcap(path)


def capture_live(interface: str, timeout: Optional[int] = 10) -> list:
    """Capture packets from a live interface for `timeout` seconds."""

    if sniff is None:
        raise RuntimeError("scapy is required for live capture; pip install scapy")

    packets = []
    def _collector(pkt):
        packets.append(pkt)
    sniff(iface=interface, prn=_collector, store=False, timeout=timeout)
    return packets


def save_json(out: Dict, path: str) -> None:
    """Save results dictionary to JSON file path."""

    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)


def _cli() -> None:
    """Command-line interface for running the Sentinel detection engine."""
    parser = argparse.ArgumentParser(description="Sentinel Phase 1 sniffer CLI")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--pcap", help="Path to pcap file to process")
    group.add_argument("--iface", help="Network interface to capture live packets from")
    parser.add_argument("--timeout", type=int, default=10, help="Capture timeout in seconds for live capture")
    parser.add_argument("--output", default="out.json", help="Output JSON path")
    parser.add_argument("--model-load", default=None, help="Path to load a pre-trained IsolationForest model")
    parser.add_argument("--model-save", default=None, help="Path to save the trained IsolationForest model (after fitting)")
    # Alerting options
    parser.add_argument("--smtp-server", default=None, help="SMTP server for email alerts")
    parser.add_argument("--smtp-port", type=int, default=587, help="SMTP port for email alerts")
    parser.add_argument("--smtp-user", default=None, help="SMTP username for email alerts")
    parser.add_argument("--smtp-password", default=None, help="SMTP password for email alerts")
    parser.add_argument("--email-from", default=None, help="Sender email address for alerts")
    parser.add_argument("--email-to", default=None, help="Recipient email address for alerts")
    args = parser.parse_args()

    if args.pcap:
        logger.info("Reading pcap: %s", args.pcap)
        packets = read_pcap(args.pcap)
    else:
        logger.info("Capturing on interface: %s for %ds", args.iface, args.timeout)
        packets = capture_live(args.iface, timeout=args.timeout)

    detector: Optional[AnomalyDetector] = None
    if args.model_load:
        logger.info("Loading model from %s", args.model_load)
        detector = AnomalyDetector.load(args.model_load)

    # Setup alert manager
    alert_manager = AlertManager(
        smtp_server=args.smtp_server,
        smtp_port=args.smtp_port,
        smtp_user=args.smtp_user,
        smtp_password=args.smtp_password,
        email_from=args.email_from,
        email_to=args.email_to,
    )

    out = process_packets(packets, detector=detector, alert_manager=alert_manager)

    # If model wasn't loaded and user requested save, train a fresh model and save it
    if not args.model_load and args.model_save:
        logger.info("Saving trained model to %s", args.model_save)
        # fit on current dataset and save
        # Note: build and fit using the actual captured packets below
        # Re-extract flows and fit then save
        extractor = FlowExtractor()
        extractor.add_packets(packets)
        flows = extractor.flows()
        df_live = FeatureBuilder.build(flows)
        tmp_detector = AnomalyDetector()
        tmp_detector.fit(df_live)
        tmp_detector.save(args.model_save)
    save_json(out, args.output)
    logger.info("Wrote results to %s", args.output)


if __name__ == "__main__":
    _cli()
