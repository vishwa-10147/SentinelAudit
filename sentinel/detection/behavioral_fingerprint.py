"""
BehavioralFingerprint: Per-device baseline and drift detection.
"""
from typing import Dict, Any

class BehavioralFingerprint:
    def __init__(self):
        self.device_profiles: Dict[str, Dict[str, float]] = {}

    def update(self, ip: str, features: Dict[str, float]):
        if ip not in self.device_profiles:
            self.device_profiles[ip] = features.copy()
        else:
            for k, v in features.items():
                self.device_profiles[ip][k] = 0.9 * self.device_profiles[ip][k] + 0.1 * v

    def check_drift(self, ip: str, current_features: Dict[str, float]):
        if ip not in self.device_profiles:
            return False, '', 0.0
        baseline = self.device_profiles[ip]
        deviation = sum(abs(current_features[k] - baseline.get(k, 0)) for k in current_features) / (len(current_features) or 1)
        has_drift = deviation > 0.2  # Example threshold
        return has_drift, 'Drift detected' if has_drift else '', deviation
