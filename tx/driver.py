# swing/Vcm, slew kernel

import numpy as np
from typing import Sequence

def apply_swing(waveform: Sequence[float], swing: float) -> np.ndarray:
    """
    Scale waveform to desired output swing (peak-to-peak voltage).

    Args:
        waveform: array of waveform samples
        swing: desired peak-to-peak swing (volts)

    Returns:
        Scaled waveform with specified swing
    """
    max_abs = np.max(np.abs(waveform))
    return np.array(waveform) * (swing / (2 * max_abs))

def apply_vcm(waveform: Sequence[float], vcm: float) -> np.ndarray:
    """
    Add common-mode voltage (Vcm) to waveform.

    Args:
        waveform: array of waveform samples
        vcm: common-mode voltage to add (volts)

    Returns:
        Waveform with Vcm added
    """
    return np.array(waveform) + vcm
