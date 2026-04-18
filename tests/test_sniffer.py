"""Pytest unit tests for sentinel.detection.sniffer.

These tests avoid live packet capture and instead exercise the
feature builder, anomaly detector, MITRE mapper, and CLI-free
processing paths.
"""
import os

import pandas as pd

from sentinel.detection.sniffer import (
    Flow,
    FeatureBuilder,
    AnomalyDetector,
    MitreMapper,
    process_packets,
)


def test_feature_builder_with_flows() -> None:
    f1 = Flow("1.1.1.1", 123, "2.2.2.2", 80, "TCP", 0.0, 1.0, 10, 1000)
    f2 = Flow("3.3.3.3", None, "4.4.4.4", None, "UDP", 0.0, 2.0, 5, 500)
    df = FeatureBuilder.build([f1, f2])
    assert list(df.columns) == ["packet_count", "byte_count", "duration", "avg_pkt_size"]
    assert int(df.iloc[0]["packet_count"]) == 10
    assert float(df.iloc[0]["avg_pkt_size"]) == 100.0


def test_process_packets_empty() -> None:
    out = process_packets([])
    assert "generated_at" in out
    assert out["results"] == []


def test_anomaly_detector_and_persistence(tmp_path) -> None:
    # Create dataset with one obvious outlier
    data = pd.DataFrame(
        {
            "packet_count": [10] * 9 + [1000],
            "byte_count": [100] * 9 + [10_000_000],
            "duration": [1.0] * 10,
            "avg_pkt_size": [10.0] * 9 + [10000.0],
        }
    )

    detector = AnomalyDetector(contamination=0.1)
    detector.fit(data)
    preds = detector.predict(data)
    assert preds.sum() >= 1

    model_file = os.path.join(tmp_path, "model.joblib")
    detector.save(model_file)
    loaded = AnomalyDetector.load(model_file)
    assert loaded._fitted is True
    preds2 = loaded.predict(data)
    assert preds2.tolist() == preds.tolist()


def test_mitre_mapper() -> None:
    f = Flow("1.1.1.1", 123, "2.2.2.2", 8080, "TCP", 0, 1, 2000, 1_000_000)
    feats = {"packet_count": 2000, "avg_pkt_size": 100, "byte_count": 2_000_000}
    mappings = MitreMapper.map(f, feats, True)
    assert isinstance(mappings, list)
    assert len(mappings) >= 1
