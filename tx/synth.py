"""
Symbol-to-waveform synthesis at Tx samples per symbol (sps)
"""

import numpy as np
from typing import Sequence, Callable, Optional, Tuple
from .dac import DAC


def synthesize_waveform(
    symbols: Sequence[float],
    dac: DAC,
    symbol_rate: float,
    sim_sample_rate: Optional[float] = None,
    jitter: Optional[Callable[[np.ndarray], np.ndarray]] = None
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Convert symbols to waveform samples using the DAC, apply jitter if specified.
    If sim_sample_rate is provided (Sa/s), the output is resampled to that rate;
    otherwise output remains at the DAC sample rate (dac.sps * symbol_rate).
    """
    # Process symbols through the DAC (produces DAC-rate samples)
    waveform_dac = dac.process(symbols)
    dac_fs = dac.sps * symbol_rate  # samples per second at DAC

    # Apply jitter at sample level if provided
    if jitter is not None:
        waveform_dac = jitter(waveform_dac)

    n_samples_dac = len(waveform_dac)
    t_dac = np.arange(n_samples_dac) / dac_fs

    # If no sim sample rate requested, return DAC-rate waveform
    if sim_sample_rate is None:
        return waveform_dac, t_dac

    # Resample (interpolate) to simulation sample rate
    sim_fs = float(sim_sample_rate)
    n_symbols = len(symbols)
    sim_sps = sim_fs / symbol_rate
    n_samples_sim = int(round(n_symbols * sim_sps))
    t_sim = np.arange(n_samples_sim) / sim_fs

    # linear interpolation; replace with higher-order if needed
    waveform_sim = np.interp(t_sim, t_dac, waveform_dac)

    return waveform_sim, t_sim
