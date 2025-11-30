import numpy as np
from typing import Sequence


def ideal_sampler(waveform: Sequence[float], sps: int) -> np.ndarray:
	"""
	Sample input waveform at symbol rate (ideal CDR).
	Args:
		waveform: Input waveform samples.
		sps: Samples per symbol.
	Returns:
		Array of symbol samples.
	"""
	return np.array(waveform)[::sps]

def bang_bang_phase_detector(waveform: Sequence[float], sps: int, threshold: float = 0.0) -> np.ndarray:
	"""
	Bang-bang phase detector for NRZ using Early (E), Mid (M), Late (L) samples.
	Args:
		waveform: Input waveform samples.
		rx_adc_sps: Receiver ADC samples per symbol.
		threshold: Slicing threshold for decision.
	Returns:
		Array of phase errors (1: early, -1: late, 0: correct).
	"""
	# For backward compatibility, allow sps as rx_adc_sps
	rx_adc_sps = sps
	errors = []
	waveform = np.array(waveform)
	half_sps = rx_adc_sps // 2
	n_symbols = (len(waveform) - rx_adc_sps) // rx_adc_sps
	for i in range(1, n_symbols):
		# Sample indices
		mid_idx = i * rx_adc_sps + half_sps
		early_idx = mid_idx - half_sps
		late_idx = mid_idx + half_sps
		if late_idx >= len(waveform):
			break
		# Decisions
		early_val = waveform[early_idx]
		mid_val = waveform[mid_idx]
		late_val = waveform[late_idx]
		early = 1 if early_val > threshold else 0
		mid = 1 if mid_val > threshold else 0
		late = 1 if late_val > threshold else 0
		# Bang-bang logic: compare early and late to mid
		if early != mid:
			phase = 1  # Early sample differs: clock is early
		elif late != mid:
			phase = -1 # Late sample differs: clock is late
		else:
			phase = 0  # No transition
		errors.append(phase)
		print(f"E={early_val:.3f} M={mid_val:.3f} L={late_val:.3f} | E_dec={early} M_dec={mid} L_dec={late} | phase={phase}")
	return np.array(errors)

def hogge_phase_detector(waveform: Sequence[float], sps: int) -> np.ndarray:
	"""
	Hogge phase detector for NRZ. Returns phase error at each symbol.
	Args:
		waveform: Input waveform samples.
		sps: Samples per symbol.
	Returns:
		Array of phase errors.
	"""
	errors = []
	for i in range(sps, len(waveform)-sps, sps):
		mid = waveform[i]
		early = waveform[i - sps//2]
		late = waveform[i + sps//2] if (i + sps//2) < len(waveform) else mid
		error = (early - late) * mid
		errors.append(error)
	return np.array(errors)

def simple_loop_filter(errors: Sequence[float], alpha: float = 0.01) -> np.ndarray:
	"""
	Simple first-order loop filter for phase error integration.
	Args:
		errors: Sequence of phase errors.
		alpha: Filter coefficient.
	Returns:
		Filtered phase estimate.
	"""
	phase = 0.0
	out = []
	for e in errors:
		phase += alpha * e
		out.append(phase)
	return np.array(out)


