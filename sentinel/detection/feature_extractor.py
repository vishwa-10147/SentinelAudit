"""
FeatureExtractor: Extracts 24 statistical features from a flow.
"""
from typing import Dict, Any
import numpy as np

class FeatureExtractor:
    @staticmethod
    def extract(flow: Dict[str, Any]) -> Dict[str, float]:
        # Placeholder: implement all 24 features as per README
        features = {
            'packet_count': len(flow['packets']),
            'byte_count': sum(len(pkt) for pkt in flow['packets']),
            'duration_seconds': flow['packets'][-1].time - flow['packets'][0].time if len(flow['packets']) > 1 else 0,
            'avg_packet_size': np.mean([len(pkt) for pkt in flow['packets']]) if flow['packets'] else 0,
            'std_packet_size': np.std([len(pkt) for pkt in flow['packets']]) if flow['packets'] else 0,
            # ... add the rest of the 24 features ...
        }
        return features
