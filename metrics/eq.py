
import numpy as np
from typing import Sequence, Tuple

def mmse_taps(rx_symbols: Sequence[float], tx_symbols: Sequence[float], n_taps: int) -> np.ndarray:
	"""
	Calculate MMSE FFE taps.
	Args:
		rx_symbols: Received symbol sequence.
		tx_symbols: Transmitted symbol sequence.
		n_taps: Number of taps.
	Returns:
		Array of MMSE tap weights.
	"""
	# Build Toeplitz matrix for FFE
	from scipy.linalg import toeplitz
	X = toeplitz(rx_symbols, np.zeros(n_taps))
	y = np.array(tx_symbols)
	# Least squares solution
	taps, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
	return taps

def evm(rx_symbols: Sequence[float], tx_symbols: Sequence[float]) -> float:
	"""
	Calculate Error Vector Magnitude (EVM).
	Args:
		rx_symbols: Received symbol sequence.
		tx_symbols: Transmitted symbol sequence.
	Returns:
		EVM as percentage.
	"""
	rx_symbols = np.array(rx_symbols)
	tx_symbols = np.array(tx_symbols)
	error = rx_symbols - tx_symbols
	return 100 * np.sqrt(np.mean(error**2)) / np.mean(np.abs(tx_symbols))

def snr(rx_symbols: Sequence[float], tx_symbols: Sequence[float]) -> float:
	"""
	Calculate Signal-to-Noise Ratio (SNR).
	Args:
		rx_symbols: Received symbol sequence.
		tx_symbols: Transmitted symbol sequence.
	Returns:
		SNR in dB.
	"""
	rx_symbols = np.array(rx_symbols)
	tx_symbols = np.array(tx_symbols)
	signal_power = np.mean(tx_symbols**2)
	noise_power = np.mean((rx_symbols - tx_symbols)**2)
	return 10 * np.log10(signal_power / noise_power)
