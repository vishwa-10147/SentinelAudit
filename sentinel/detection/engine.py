"""
SentinelEngine: Orchestrates all detection modules.
"""
from .flow_table import FlowTable
from .feature_extractor import FeatureExtractor
from .anomaly_engine import AnomalyEngine
from .behavioral_fingerprint import BehavioralFingerprint
from .risk_engine import RiskEngine
from .mitre_mapper import MitreMapper
from .alert_logger import AlertLogger

class SentinelEngine:
    def __init__(self):
        self.flow_table = FlowTable()
        self.feature_extractor = FeatureExtractor()
        self.anomaly_engine = AnomalyEngine()
        self.behavioral_fingerprint = BehavioralFingerprint()
        self.risk_engine = RiskEngine()
        self.mitre_mapper = MitreMapper()
        self.alert_logger = AlertLogger()

    def process_packet(self, packet, key, timestamp):
        self.flow_table.add_packet(key, packet, timestamp)
        expired = self.flow_table.get_expired_flows(timestamp)
        for flow_key, flow in expired.items():
            features = self.feature_extractor.extract(flow)
            self.anomaly_engine.warmup(features)
            anomaly = self.anomaly_engine.predict(features)
            ip = flow_key[0]
            self.behavioral_fingerprint.update(ip, features)
            drift, drift_reason, deviation = self.behavioral_fingerprint.check_drift(ip, features)
            risk = self.risk_engine.score(anomaly['anomaly_score'], drift, 1 if anomaly['is_anomalous'] else 0)
            mitre = self.mitre_mapper.map_threat('port_scanning')  # Example, replace with real logic
            alert = {
                'flow_key': flow_key,
                'features': features,
                'anomaly': anomaly,
                'drift': drift,
                'risk': risk,
                'mitre': mitre
            }
            if risk['severity'] in ['Critical', 'High']:
                self.alert_logger.log_alert(alert)
            self.alert_logger.log_device_profile({'ip': ip, 'features': features})
