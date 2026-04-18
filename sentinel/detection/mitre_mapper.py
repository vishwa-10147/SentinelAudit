"""
MitreMapper: Map threat patterns to MITRE ATT&CK techniques.
"""
from typing import Dict, Any

MITRE_MAP = {
    'port_scanning': {'id': 'T1046', 'name': 'Network Service Discovery'},
    'dns_anomaly': {'id': 'T1071', 'name': 'Application Layer Protocol'},
    'unusual_outbound': {'id': 'T1041', 'name': 'Exfiltration Over C2 Channel'},
    'rogue_device': {'id': 'T1200', 'name': 'Hardware Additions'},
    'brute_force': {'id': 'T1110', 'name': 'Brute Force'},
    'data_staged': {'id': 'T1074', 'name': 'Data Staged'},
}

class MitreMapper:
    @staticmethod
    def map_threat(threat_type: str) -> Dict[str, str]:
        return MITRE_MAP.get(threat_type, {'id': '', 'name': ''})
