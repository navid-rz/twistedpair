
import numpy as np
from metrics.ber import empirical_ber, q_factor_ber
from metrics.eye import fold_to_eye, eye_height_width, pam4_eye_heights
from metrics.eq import mmse_taps, evm, snr

def test_empirical_ber():
	tx_bits = np.array([0, 1, 1, 0, 1])
	rx_bits = np.array([0, 1, 0, 0, 1])
	ber = empirical_ber(rx_bits, tx_bits)
	assert 0 <= ber <= 1

def test_q_factor_ber():
	ber = q_factor_ber(6.0)
	assert 0 <= ber <= 1

def test_fold_to_eye():
	waveform = np.tile(np.array([1, -1]), 8)
	eye = fold_to_eye(waveform, 2)
	assert eye.shape == (8, 2)

def test_eye_height_width():
	eye = np.ones((8, 2))
	height, width = eye_height_width(eye)
	assert isinstance(height, float)
	assert isinstance(width, float)

def test_pam4_eye_heights():
	eye = np.tile(np.array([-3, -1, 1, 3]), (8, 1))
	heights = pam4_eye_heights(eye)
	assert len(heights) == 3

def test_mmse_taps():
	rx = np.ones(10)
	tx = np.ones(10)
	taps = mmse_taps(rx, tx, 3)
	assert taps.shape[0] == 3

def test_evm_snr():
	rx = np.ones(10)
	tx = np.ones(10)
	assert evm(rx, tx) == 0
	assert snr(rx, tx) > 0
