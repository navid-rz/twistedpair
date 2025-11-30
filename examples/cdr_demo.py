import numpy as np
import matplotlib.pyplot as plt
from rx.cdr import bang_bang_phase_detector
from bit_utils.core import prbs

def generate_alternating_waveform(n_symbols, sps, swing=1.0, vcm=0.0, offset=0):
    """
    Generate a waveform for 101010... pattern with optional clock offset.
    Args:
        n_symbols: Number of symbols
        sps: Samples per symbol
        swing: Amplitude swing
        vcm: Common mode voltage
        offset: Clock offset in samples (0 = aligned)
    Returns:
        waveform: numpy array
    """
    bits = np.array([(i % 2) for i in range(n_symbols)])
    symbols = swing * (2 * bits - 1) + vcm
    waveform = np.repeat(symbols, sps)
    if offset > 0:
        waveform = np.roll(waveform, offset)
    return waveform

def main():
    # Option: input_format = 'prbs' or 'alternating'
    input_format = 'alternating'  # Change to 'alternating' for +1/-1 training sequence

    n_symbols = 10
    sps = 16
    swing = 1.0
    vcm = 0.0
    clock_offset = 5  # samples
    threshold = 0.0
    noise_sigma = 0.01
    jitter_sigma = 2  # samples
    prbs_order = 23
    prbs_seed = 0x7FFFFFFF

    if input_format == 'prbs':
        bits = prbs(prbs_order, n_symbols, seed=prbs_seed)
        symbols = swing * (2 * bits - 1) + vcm
    elif input_format == 'alternating':
        # +1/-1 alternating sequence
        symbols = swing * np.array([1 if i % 2 == 0 else -1 for i in range(n_symbols)]) + vcm
    else:
        raise ValueError("input_format must be 'prbs' or 'alternating'")

    waveform = np.repeat(symbols, sps)
    if clock_offset > 0:
        waveform = np.roll(waveform, clock_offset)

    # Add noise
    waveform += np.random.normal(0, noise_sigma, size=waveform.shape)

    # Add jitter (randomly shift sampling points)
    jitter = np.random.normal(0, jitter_sigma, size=n_symbols)
    sample_idx = np.arange(0, n_symbols * sps, sps) + jitter.astype(int)
    sample_idx = np.clip(sample_idx, 0, len(waveform)-1)

    # Use bang-bang phase detector for phase error output
    errors = bang_bang_phase_detector(waveform, sps, threshold=threshold)

    # Plot only first n_symbols
    plot_len = n_symbols * sps
    fig, ax1 = plt.subplots(figsize=(10, 5))
    t = np.arange(plot_len) / sps
    ax1.plot(t, waveform[:plot_len], label='Waveform')
    # Mark (jittered) sampling points
    ax1.plot(t[sample_idx], waveform[sample_idx], 'ko', label='Sampling Points')
    # Add threshold line
    ax1.axhline(threshold, color='g', linestyle='--', label='Threshold')
    ax1.set_xlabel('Symbol Index')
    ax1.set_ylabel('Amplitude', color='b')
    ax1.tick_params(axis='y', labelcolor='b')

    ax2 = ax1.twinx()
    error_t = np.arange(1, len(errors)+1)
    ax2.step(error_t, errors, where='mid', color='r', label='Phase Error')
    ax2.set_ylabel('Phase Error', color='r')
    ax2.tick_params(axis='y', labelcolor='r')
    ax2.set_ylim([-1.1, 1.1])

    plt.title(f'Bang-Bang Phase Detector Demo (input: {input_format}, Clock Offset: {clock_offset} samples, Noise: {noise_sigma}, Jitter: {jitter_sigma})')
    fig.tight_layout()
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    plt.show()

if __name__ == "__main__":
    main()
