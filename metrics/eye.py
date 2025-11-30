
import numpy as np
from typing import Sequence, Tuple

def fold_to_eye(waveform: Sequence[float], sps: int) -> np.ndarray:
	"""
	Fold waveform to eye diagram (2D array: symbol x sample).
	Args:
		waveform: Input waveform samples.
		sps: Samples per symbol.
	Returns:
		Eye diagram array.
	"""
	n_symbols = len(waveform) // sps
	eye = np.array(waveform[:n_symbols * sps]).reshape((n_symbols, sps))
	return eye


def eye_height_width(eye: np.ndarray) -> Tuple[float, float]:
	"""
	Calculate eye height and width from eye diagram (NRZ).
	Args:
		eye: Eye diagram array.
	Returns:
		(height, width) tuple.
	"""
	# Height: difference between mean of top/bottom samples
	top = np.mean(eye[:, eye.shape[1]//2:])
	bottom = np.mean(eye[:, :eye.shape[1]//2])
	height = top - bottom
	# Width: number of samples above threshold at center crossing
	center = eye.shape[1] // 2
	threshold = (top + bottom) / 2
	width = np.sum(np.abs(eye[:, center] - threshold) < (height / 2)) / eye.shape[0]
	return height, width

def pam4_eye_heights(eye: np.ndarray, thresholds: Sequence[float] = (-2, 0, 2)) -> Tuple[float, float, float]:
	"""
	Calculate the three PAM4 eye heights from the eye diagram.
	Args:
		eye: Eye diagram array (symbols x samples).
		thresholds: Decision thresholds for PAM4 (default: -2, 0, 2).
	Returns:
		Tuple of three eye heights (bottom, middle, top).
	"""
	center = eye.shape[1] // 2
	# For each region between thresholds, compute mean difference
	samples = eye[:, center]
	# Bottom eye: between lowest and middle threshold
	bottom_eye = np.mean(samples[(samples > thresholds[0]) & (samples < thresholds[1])]) - np.mean(samples[samples < thresholds[0]])
	# Middle eye: between middle thresholds
	middle_eye = np.mean(samples[(samples > thresholds[1]) & (samples < thresholds[2])]) - np.mean(samples[(samples > thresholds[0]) & (samples < thresholds[1])])
	# Top eye: above highest threshold
	top_eye = np.mean(samples[samples > thresholds[2]]) - np.mean(samples[(samples > thresholds[1]) & (samples < thresholds[2])])
	return bottom_eye, middle_eye, top_eye

def bathtub_curve(eye: np.ndarray, thresholds: Sequence[float]) -> np.ndarray:
	"""
	Calculate a simple bathtub curve (eye opening vs threshold).
	Args:
		eye: Eye diagram array.
		thresholds: List of thresholds to test.
	Returns:
		Array of eye openings for each threshold.
	"""
	openings = []
	center = eye.shape[1] // 2
	for th in thresholds:
		opening = np.sum(np.abs(eye[:, center] - th) < 0.5) / eye.shape[0]
		openings.append(opening)
	return np.array(openings)
