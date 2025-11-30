import numpy as np
from scipy.signal import welch
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from scipy.signal import welch
from typing import Sequence, Optional

def plot_symbols_streams(
	symbols_list: Sequence[Sequence[float]],
	legends: Sequence[str],
	title: str = "Symbol Streams",
	xlabel: str = "Symbol Index",
	ylabel: str = "Symbol Value",
	save_path: Optional[str] = None
) -> None:
	"""
	Plot multiple symbol streams overlapped, with legends.
	Args:
		symbols_list: List of symbol sequences to plot.
		legends: List of legend labels for each stream.
		title: Plot title.
		xlabel: X axis label.
		ylabel: Y axis label.
		save_path: If specified, save plot to this path.
	"""
	plt.figure()
	for symbols, label in zip(symbols_list, legends):
		plt.plot(symbols, label=label)
	plt.title(title)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.legend()
	plt.grid(True)
	if save_path:
		plt.savefig(save_path)
	plt.show()


def plot_psd(
	waveform: Sequence[float],
	sample_rate: float,
	title: str = "Power Spectral Density",
	save_path: Optional[str] = None
) -> None:
	"""
	Plot the Power Spectral Density (PSD) of a waveform using Welch's method.
	Args:
		waveform: Sequence of waveform samples.
		sample_rate: Sample rate in Hz.
		title: Plot title.
		save_path: If specified, save plot to this path.
	"""
	f, Pxx = welch(waveform, fs=sample_rate, nperseg=min(1024, len(waveform)))
	plt.figure()
	plt.semilogy(f/1e9, Pxx)  # Frequency in GHz
	plt.title(title)
	plt.xlabel("Frequency (GHz)")
	plt.ylabel("PSD (V^2/Hz)")
	plt.grid(True)
	if save_path:
		plt.savefig(save_path)
	plt.show()

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from typing import Sequence, Optional
from typing import Optional

def plot_waveform(
	waveform: Sequence[float],
	time: Optional[Sequence[float]] = None,
	title: str = "Waveform",
	xlabel: str = "Time (s)",
	ylabel: str = "Amplitude (V)",
	save_path: Optional[str] = None
) -> None:
	"""
	Plot a static waveform vs time. Optionally save to file.
	Args:
		waveform: Sequence of waveform samples.
		time: Sequence of time samples (same length as waveform).
		title: Plot title.
		xlabel: X-axis label (default: Time (s)).
		ylabel: Y-axis label (default: Amplitude (V)).
		save_path: If specified, save plot to this path.
	"""
	plt.figure()
	if time is not None:
		plt.plot(time, waveform)
	else:
		plt.plot(waveform)
	plt.title(title)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.grid(True)
	if save_path:
		plt.savefig(save_path)
	plt.show()

def plot_eye(
    eye: Sequence[Sequence[float]],
    sim_sample_rate: Optional[float] = None,
    title: str = "Eye Diagram",
    save_path: Optional[str] = None
) -> None:
	"""
	Plot an eye diagram from a 2D array. X-axis is time if sim_sample_rate is provided.
	Args:
		eye: 2D array-like (traces x samples) or list of 1D traces.
		sim_sample_rate: If provided (samples/second), x-axis will be time in seconds.
		title: Plot title.
		save_path: If specified, save plot to this path.
	"""
	plt.figure()
	eye_arr = np.asarray(eye)
	if eye_arr.ndim == 1:
		eye_arr = eye_arr[np.newaxis, :]
	n_samples = eye_arr.shape[1]

	if sim_sample_rate is not None and sim_sample_rate > 0:
		t = np.arange(n_samples) / float(sim_sample_rate)
		for trace in eye_arr:
			plt.plot(t, trace, color='blue', alpha=0.2)
		plt.xlabel("Time (s)")
	else:
		for trace in eye_arr:
			plt.plot(trace, color='blue', alpha=0.2)
		plt.xlabel("Sample")

	plt.title(title)
	plt.ylabel("Amplitude")
	plt.grid(True)
	if save_path:
		plt.savefig(save_path)
	plt.show()

def animate_waveform_evolution(waveforms: Sequence[Sequence[float]], interval: int = 100, title: str = "Waveform Evolution", save_path: Optional[str] = None) -> None:
	"""
	Animate a sequence of waveforms (e.g., pulse propagating through a link). Optionally save animation to file.
	Args:
		waveforms: List of waveform samples at each stage/time.
		interval: Delay between frames in ms.
		title: Animation title.
		save_path: If specified, save animation to this path (as .mp4 or .gif).
	"""
	fig, ax = plt.subplots()
	line, = ax.plot([], [], lw=2)
	ax.set_xlim(0, len(waveforms[0]))
	ax.set_ylim(min(map(min, waveforms)), max(map(max, waveforms)))
	ax.set_title(title)
	ax.set_xlabel("Sample")
	ax.set_ylabel("Amplitude")
	ax.grid(True)

	def init():
		line.set_data([], [])
		return line,

	def update(frame):
		line.set_data(range(len(waveforms[frame])), waveforms[frame])
		return line,

	ani = FuncAnimation(fig, update, frames=len(waveforms), init_func=init, blit=True, interval=interval)
	if save_path:
		ani.save(save_path)
	plt.show()
