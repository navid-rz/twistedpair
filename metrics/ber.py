
import numpy as np
from typing import Sequence, Optional

def empirical_ber(rx_bits: Sequence[int], tx_bits: Sequence[int]) -> float:
	"""
	Calculate empirical bit error rate (BER).
	Args:
		rx_bits: Received bits (0/1).
		tx_bits: Transmitted bits (0/1).
	Returns:
		BER as float.
	"""
	rx_bits = np.array(rx_bits)
	tx_bits = np.array(tx_bits)
	errors = np.sum(rx_bits != tx_bits)
	return errors / len(tx_bits)

def q_factor_ber(q: float) -> float:
	"""
	Estimate BER from Q-factor (Gaussian assumption).
	Args:
		q: Q-factor (signal-to-noise ratio).
	Returns:
		Estimated BER.
	"""
	from scipy.special import erfc
	return 0.5 * erfc(q / np.sqrt(2))
