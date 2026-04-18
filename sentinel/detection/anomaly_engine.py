"""
AnomalyEngine: Z-score and Isolation Forest anomaly detection.
"""
from typing import Dict, Any
import numpy as np
from sklearn.ensemble import IsolationForest

class AnomalyEngine:
    def __init__(self):
        self.baseline = []
        self.model = IsolationForest()
        self.fitted = False

    def warmup(self, features: Dict[str, float]):
        self.baseline.append(features)
        if len(self.baseline) >= 50 and not self.fitted:
            X = np.array([list(f.values()) for f in self.baseline])
            self.model.fit(X)
            self.fitted = True

    def z_score(self, features: Dict[str, float]) -> float:
        if not self.baseline:
            return 0.0
        arr = np.array([list(f.values()) for f in self.baseline])
        mean = arr.mean(axis=0)
        std = arr.std(axis=0)
        vals = np.array(list(features.values()))
        z = np.abs((vals - mean) / (std + 1e-9))
        return float(np.max(z))

    def predict(self, features: Dict[str, float]) -> Dict[str, Any]:
        z = self.z_score(features)
        is_anom = z > 3.0
        score = 0.0
        reason = ''
        if self.fitted:
            X = np.array([list(features.values())])
            pred = self.model.predict(X)[0]
            score = -self.model.decision_function(X)[0]
            is_anom = pred == -1
            reason = 'IsolationForest' if is_anom else 'Normal'
        else:
            reason = 'Z-score' if is_anom else 'Normal'
        return {'is_anomalous': is_anom, 'anomaly_score': score, 'reason': reason}
