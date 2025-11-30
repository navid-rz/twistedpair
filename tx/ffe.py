# Symbol-rate FFE (pre-emphasis), tap normalization

import numpy as np

def apply_ffe(symbols, taps):
    """Apply symbol-rate FFE to input symbols."""
    return np.convolve(symbols, taps, mode='same')

def normalize_taps(taps):
    """Normalize FFE taps so their sum is 1."""
    s = sum(taps)
    return [t/s for t in taps]
