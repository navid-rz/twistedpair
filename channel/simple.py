

import numpy as np
from typing import Sequence
from config.schema import ChannelCfg

def simple_channel(waveform: Sequence[float], cfg: ChannelCfg) -> np.ndarray:
	"""
	Simple channel: FIR ISI, AWGN, fixed loss, and delay using ChannelCfg.
	Args:
		waveform: Input waveform samples.
		cfg: ChannelCfg dataclass instance.
	Returns:
		Output waveform after channel effects.
	"""
	isi_taps = cfg.isi_taps if cfg.isi_taps is not None else [1.0]
	awgn_sigma = cfg.awgn_sigma if cfg.awgn_sigma is not None else 0.0
	delay = int(cfg.delay) if cfg.delay is not None else 0
	fixed_loss_db = cfg.fixed_loss_db if cfg.fixed_loss_db is not None else 0.0
	gain = 10 ** (-fixed_loss_db / 20)
	# FIR ISI
	out = np.convolve(waveform, isi_taps, mode='same')
	# Gain
	out *= gain
	# Delay
	if delay > 0:
		out = np.concatenate([np.zeros(delay), out[:-delay]])
	# AWGN
	if awgn_sigma > 0:
		out += np.random.normal(0, awgn_sigma, size=out.shape)
	return out

def copper_channel(waveform: Sequence[float], cfg: ChannelCfg) -> np.ndarray:
	"""
	Copper channel: frequency-dependent loss profile using ChannelCfg.
	Args:
		waveform: Input waveform samples.
		cfg: ChannelCfg dataclass instance.
	Returns:
		Output waveform after copper channel effects.
	"""
	# Calculate frequency-dependent loss
	alpha = cfg.alpha_db_per_in_ghz if cfg.alpha_db_per_in_ghz is not None else 0.5
	length = cfg.length_in if cfg.length_in is not None else 20.0
	f_ref = cfg.f_ref_ghz if cfg.f_ref_ghz is not None else 10.0
	fixed_loss_db = cfg.fixed_loss_db if cfg.fixed_loss_db is not None else 0.0
	awgn_sigma = cfg.awgn_sigma if cfg.awgn_sigma is not None else 0.0
	delay = int(cfg.delay) if cfg.delay is not None else 0

	# Apply fixed loss
	gain = 10 ** (-fixed_loss_db / 20)
	out = np.array(waveform) * gain

	# Apply frequency-dependent loss (simple lowpass filter)
	# For demo: use a single-pole IIR filter to mimic copper roll-off
	# Compute cutoff frequency based on alpha, length, and f_ref
	cutoff = f_ref / (1 + alpha * length)
	# Normalize cutoff to Nyquist (assume sps=1 for demo)
	norm_cutoff = min(0.5, cutoff / (2 * f_ref))
	# Simple IIR lowpass
	b = [norm_cutoff]
	a = [1, norm_cutoff - 1]
	for i in range(1, len(out)):
		out[i] = b[0] * out[i] + a[1] * out[i-1]

	# Delay
	if delay > 0:
		out = np.concatenate([np.zeros(delay), out[:-delay]])
	# AWGN
	if awgn_sigma > 0:
		out += np.random.normal(0, awgn_sigma, size=out.shape)
	return out
