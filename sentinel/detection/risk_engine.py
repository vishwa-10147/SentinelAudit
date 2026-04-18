"""
RiskEngine: Unified risk scoring for flows.
"""
from typing import Dict, Any

class RiskEngine:
    def __init__(self):
        pass

    def score(self, anomaly_score: float, drift: bool, threat_indicators: int) -> Dict[str, Any]:
        risk_score = int((anomaly_score * 0.4 + (0.3 if drift else 0) + threat_indicators * 0.3) * 100)
        if risk_score >= 75:
            severity = 'Critical'
        elif risk_score >= 50:
            severity = 'High'
        elif risk_score >= 25:
            severity = 'Medium'
        else:
            severity = 'Low'
        return {'risk_score': risk_score, 'severity': severity}
