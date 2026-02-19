#!/usr/bin/env python3
"""
Visual Learning Engine - Neural Optimization Engine
Schmidhuber-inspired neural compression and LSTM-based sequential pattern memory.
"""

import json
import logging
import sys
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

# Ensure local imports work
sys.path.append(os.path.dirname(__file__))
from visual_types import VisualPattern

class AdaptiveContextEngine:
    """Handles neural compression and sequential memory optimization"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.lstm_memory = {}  # LSTM-inspired sequential pattern memory
        self.compression_cache = {}  # Neural compression for learned patterns
        self.meta_learning_patterns = {}  # Patterns that improve learning itself

    async def compress_pattern(self, pattern: VisualPattern) -> Dict[str, Any]:
        """Compress visual pattern using neural compression techniques"""
        try:
            original_text = f"{pattern.description} {json.dumps(pattern.extracted_features)}"
            original_size = len(original_text.encode('utf-8'))

            compressed_features = await self._neural_compress_features(pattern.extracted_features)
            compressed_description = await self._compress_text(pattern.description)

            compressed_text = f"{compressed_description} {json.dumps(compressed_features)}"
            compressed_size = len(compressed_text.encode('utf-8'))
            compression_ratio = original_size / max(compressed_size, 1)

            return {
                'id': pattern.pattern_id,
                'description': compressed_description,
                'features': compressed_features,
                'compression_ratio': compression_ratio,
                'original_size': original_size,
                'compressed_size': compressed_size,
                'category': pattern.category,
                'confidence': pattern.confidence_score
            }
        except Exception as e:
            self.logger.warning(f"Compression failed for pattern {pattern.pattern_id}: {e}")
            return {
                'description': pattern.description,
                'features': pattern.extracted_features,
                'compression_ratio': 1.0,
                'category': pattern.category,
                'confidence': pattern.confidence_score
            }

    async def update_lstm_memory(self, category: str, compressed_pattern: Dict[str, Any]):
        """
        Update LSTM-inspired sequential memory using REAL gating math.
        
        Logic:
        - Input Gate (i): Decides how much new info to let in based on Confidence + Compression Ratio.
        - Forget Gate (f): Decides how much history to keep based on Time Decay + Sequence Saturation.
        - Cell State (c): The long-term memory.
        """
        import numpy as np
        
        # Sigmoid activation function
        def sigmoid(x):
            return 1 / (1 + np.exp(-x))

        try:
            if category not in self.lstm_memory:
                self.lstm_memory[category] = {
                    'sequence': [],
                    'cell_state': 0.5, # Initial neutral state
                    'last_updated': datetime.now(),
                }

            memory = self.lstm_memory[category]
            
            # 1. Calculate Inputs
            # Normalize confidence (0-1) and compression (assume max 5x for normalization)
            conf_input = compressed_pattern.get('confidence', 0.5)
            comp_input = min(compressed_pattern.get('compression_ratio', 1.0) / 5.0, 1.0)
            
            # 2. Input Gate (i_t): How important is this new pattern?
            # High confidence + High compression = High Input
            input_gate = sigmoid((conf_input * 2.0) + (comp_input * 1.5) - 1.0)
            
            # 3. Forget Gate (f_t): How much old stuff do we keep?
            # Time decay: Longer since last update = More forgetting
            time_delta = (datetime.now() - memory['last_updated']).total_seconds() / 3600 # Hours
            forget_gate = sigmoid(1.0 - (time_delta * 0.1)) 

            # 4. Update Cell State (Long-term Memory)
            # C_t = f_t * C_{t-1} + i_t * New_Input
            current_val = (conf_input + comp_input) / 2 # The "value" of current item
            memory['cell_state'] = (forget_gate * memory['cell_state']) + (input_gate * current_val)

            # 5. Append to Sequence if significant
            if input_gate > 0.4: # Filter noise
                memory['sequence'].append({
                    'pattern_id': compressed_pattern.get('id', 'unknown'),
                    'timestamp': datetime.now(),
                    'importance_weight': float(input_gate), # Store the calculated neural weight
                    'cell_state_snapshot': float(memory['cell_state'])
                })

            # Trim sequence based on Cell State (Adaptive Context Window)
            # Higher cell state = Keep more history
            max_len = int(20 + (memory['cell_state'] * 50)) 
            if len(memory['sequence']) > max_len:
                memory['sequence'] = memory['sequence'][-max_len:]

            memory['last_updated'] = datetime.now()
            
            self.logger.info(f"[LSTM] Updated {category}: Input={input_gate:.2f}, Forget={forget_gate:.2f}, State={memory['cell_state']:.2f}")

        except Exception as e:
            self.logger.warning(f"LSTM memory update failed for category {category}: {e}")

    async def _neural_compress_features(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Apply neural compression to pattern features"""
        compressed = {}
        for key, value in features.items():
            if isinstance(value, str) and len(value) > 100:
                compressed[key] = await self._compress_text(value)
            elif isinstance(value, list) and len(value) > 10:
                compressed[key] = value[:5] + [f"... {len(value) - 5} more items"]
            else:
                compressed[key] = value
        return compressed

    async def _compress_text(self, text: str) -> str:
        """Compress text using Schmidhuber-inspired methods"""
        try:
            if len(text) < 50: return text
            words = text.split()
            compressed_words = []
            stop_words = ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by']
            for word in words:
                if word.lower() in stop_words:
                    if len(compressed_words) == 0 or not compressed_words[-1].endswith(','):
                        continue
                compressed_words.append(word)
            compressed_text = ' '.join(compressed_words)
            return compressed_text if len(compressed_text) >= len(text) * 0.3 else text
        except Exception as e:
            self.logger.warning(f"Text compression failed: {e}")
            return text