
import numpy as np
from typing import Sequence

def apply_dfe(symbols: Sequence[float], taps: Sequence[float]) -> np.ndarray:
	"""
	Apply symbol-rate DFE to input symbols.
	Args:
		symbols: Input symbol sequence.
		taps: DFE tap weights (feedback taps).
	Returns:
		Equalized symbols as numpy array.
	"""
	out = np.zeros_like(symbols, dtype=float)
	for i in range(len(symbols)):
		feedback = sum(taps[j] * out[i-j-1] for j in range(min(i, len(taps))))
		out[i] = symbols[i] - feedback
	return out
