"""
AlertLogger: Writes alerts and device profiles to JSON files.
"""
import json
from typing import Any, Dict, List
import os

class AlertLogger:
    def __init__(self, alerts_path='alerts.json', profiles_path='device_profiles.json', timeline_path='risk_timeline.json'):
        self.alerts_path = alerts_path
        self.profiles_path = profiles_path
        self.timeline_path = timeline_path

    def log_alert(self, alert: Dict[str, Any]):
        self._append_json(self.alerts_path, alert)

    def log_device_profile(self, profile: Dict[str, Any]):
        self._append_json(self.profiles_path, profile)

    def log_risk_timeline(self, timeline: List[Dict[str, Any]]):
        with open(self.timeline_path, 'w') as f:
            json.dump(timeline, f, indent=2)

    def _append_json(self, path: str, entry: Dict[str, Any]):
        if not os.path.exists(path):
            with open(path, 'w') as f:
                json.dump([entry], f, indent=2)
        else:
            with open(path, 'r+') as f:
                data = json.load(f)
                data.append(entry)
                f.seek(0)
                json.dump(data, f, indent=2)
                f.truncate()
