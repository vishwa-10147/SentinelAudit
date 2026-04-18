"""
FlowTable: Stores active flows in memory, handles flow expiration.
"""
from typing import Any, Dict, Tuple
from datetime import datetime, timedelta

class FlowTable:
    def __init__(self, timeout_seconds: int = 30):
        self.flows: Dict[Tuple, Dict] = {}
        self.last_seen: Dict[Tuple, float] = {}
        self.timeout = timeout_seconds

    def add_packet(self, key: Tuple, packet: Any, timestamp: float) -> None:
        if key not in self.flows:
            self.flows[key] = {'packets': [], 'start': timestamp}
        self.flows[key]['packets'].append(packet)
        self.last_seen[key] = timestamp

    def get_expired_flows(self, now: float) -> Dict[Tuple, Dict]:
        expired = {}
        for key, last in list(self.last_seen.items()):
            if now - last > self.timeout:
                expired[key] = self.flows.pop(key)
                self.last_seen.pop(key)
        return expired
