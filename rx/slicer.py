
import numpy as np
from typing import Sequence, Union

def slicer_nrz(symbols: Sequence[float], threshold: float = 0.0) -> np.ndarray:
	"""
	Slice NRZ symbols to bits using threshold.
	Args:
		symbols: Input symbol values.
		threshold: Decision threshold (default 0).
	Returns:
		Array of bits (0/1).
	"""
	return np.array([1 if s > threshold else 0 for s in symbols])

def slicer_pam4(symbols: Sequence[float], thresholds: Sequence[float] = (-2, 0, 2)) -> np.ndarray:
	"""
	Slice PAM4 symbols to 2 bits using thresholds.
	Args:
		symbols: Input symbol values.
		thresholds: Tuple of 3 thresholds for PAM4 (-2, 0, 2 by default).
	Returns:
		Array of 2-bit tuples.
	"""
	def pam4_decision(s):
		if s < thresholds[0]: return (0,0)
		elif s < thresholds[1]: return (0,1)
		elif s < thresholds[2]: return (1,1)
		else: return (1,0)
	return np.array([pam4_decision(s) for s in symbols])
