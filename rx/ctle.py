
import numpy as np
from typing import Sequence

def ctle_fir(signal: Sequence[float], taps: Sequence[float]) -> np.ndarray:
	"""
	Apply FIR-based CTLE to input signal.
	Args:
		signal: Input waveform samples.
		taps: CTLE FIR tap weights.
	Returns:
		Equalized signal as numpy array.
	"""
	return np.convolve(signal, taps, mode='same')
