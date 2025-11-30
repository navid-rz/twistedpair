# RJ/SJ/DCD edge timing

import numpy as np
from typing import Sequence, Callable

# Jitter modeling functions
# RJ: Random Jitter (Gaussian noise)
# SJ: Sinusoidal Jitter (periodic)
# DCD: Duty Cycle Distortion (systematic offset)

def add_rj(edge_times: Sequence[float], sigma: float) -> np.ndarray:
    """
    Add random jitter (RJ: Random Jitter, Gaussian noise) to edge times.
    Args:
        edge_times: array of edge times
        sigma: standard deviation of jitter (seconds)
    Returns:
        Array of edge times with random jitter added
    """
    return np.array(edge_times) + np.random.normal(0, sigma, size=len(edge_times))

def add_sj(edge_times: Sequence[float], freq: float, amp: float) -> np.ndarray:
    """
    Add sinusoidal jitter (SJ: Sinusoidal Jitter) to edge times.
    Args:
        edge_times: array of edge times
        freq: frequency of sinusoidal jitter (Hz)
        amp: amplitude of jitter (seconds)
    Returns:
        Array of edge times with sinusoidal jitter added
    """
    return np.array(edge_times) + amp * np.sin(2 * np.pi * freq * np.array(edge_times))

def add_dcd(edge_times: Sequence[float], dcd: float) -> np.ndarray:
    """
    Add duty cycle distortion (DCD: Duty Cycle Distortion) to edge times.
    Args:
        edge_times: array of edge times
        dcd: offset to add to every other edge (seconds)
    Returns:
        Array of edge times with DCD applied
    """
    arr = np.array(edge_times)
    arr[1::2] += dcd
    return arr
