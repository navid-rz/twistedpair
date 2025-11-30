import numpy as np
from analysis.plots import plot_psd

# Create a pulse train (square wave) signal
sample_rate = 400e9  # 40 GHz
period_ps = 80      # 80 ps
period_s = period_ps * 1e-12  # seconds
samples_per_period = int(round(period_s * sample_rate))
n_periods = 200
n_samples = samples_per_period * n_periods

signal = np.tile(np.concatenate((np.ones(samples_per_period // 2), -np.ones(samples_per_period // 2))), n_periods)

print('Signal min/max:', signal.min(), signal.max())

# Plot PSD
plot_psd(signal, sample_rate, title="PSD of 80 ps Pulse Train")
