import numpy as np
from typing import Tuple, Optional


class VGA:
    """
    Simple variable gain amplifier model.

    - Gain is specified in dB (20*log10 amplitude gain).
    - AGC computes gain to map waveform peak-to-peak to target ADC full-scale (Vpp).
    - Optionally adds white gaussian noise (thermal) after gain.
    """

    def __init__(
        self,
        min_gain_db: float = -20.0,
        max_gain_db: float = 40.0,
        default_gain_db: float = 0.0,
        noise_std: float = 0.0,
    ) -> None:
        self.min_gain_db = float(min_gain_db)
        self.max_gain_db = float(max_gain_db)
        self.gain_db = float(default_gain_db)
        self.noise_std = float(noise_std)

    @staticmethod
    def _db_to_lin(gain_db: float) -> float:
        return 10.0 ** (gain_db / 20.0)

    def set_gain_db(self, gain_db: float) -> None:
        self.gain_db = float(np.clip(gain_db, self.min_gain_db, self.max_gain_db))

    def compute_agc_gain_db(
        self,
        waveform: np.ndarray,
        target_vpp: float,
        margin_db: float = 1.0,
        mode: str = "p2p",
    ) -> float:
        """
        Compute gain (dB) to map current waveform to target_vpp.

        mode:
          - 'p2p' (default): use peak-to-peak of waveform
          - 'rms' : use RMS and assume sinusoidal relation (not recommended for PAM)
        margin_db: headroom subtracted from target (positive -> leave headroom)
        """
        if mode not in ("p2p", "rms"):
            raise ValueError("mode must be 'p2p' or 'rms'")

        if mode == "p2p":
            cur_vpp = np.max(waveform) - np.min(waveform)
            if cur_vpp <= 0:
                return self.min_gain_db
            desired_lin = (target_vpp * (10 ** (-margin_db / 20.0))) / cur_vpp
        else:
            vrms = np.sqrt(np.mean((waveform - np.mean(waveform)) ** 2))
            if vrms <= 0:
                return self.min_gain_db
            # for sinusoid Vpp = 2*sqrt(2)*Vrms
            desired_lin = (target_vpp * (10 ** (-margin_db / 20.0))) / (2.0 * np.sqrt(2.0) * vrms)

        gain_db = 20.0 * np.log10(desired_lin)
        gain_db_clipped = float(np.clip(gain_db, self.min_gain_db, self.max_gain_db))
        return gain_db_clipped

    def process(
        self,
        waveform: np.ndarray,
        fs: float,
        block_size: int,
        target_vpp: float,
        attack_ms: float = 0.5,
        release_ms: float = 5.0,
        margin_db: float = 1.0,
        mode: str = "p2p",
        interp: bool = True,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute a causal AGC gain trajectory over `waveform` using block updates and
        apply the resulting per-sample gain to the waveform. This is a stateful AGC:
        it updates and stores self.gain_db as it progresses.

        Args:
            waveform: input samples (numpy array).
            fs: sampling rate of waveform (Sa/s).
            block_size: samples per AGC update block.
            target_vpp: desired peak-to-peak voltage after VGA (V).
            attack_ms/release_ms: AGC time constants (ms).
            margin_db: headroom in dB below target_vpp.
            mode: 'p2p' or 'rms' detection.
            interp: interpolate per-block gains to per-sample gains.

        Returns:
            scaled_waveform: waveform after applying per-sample gain.
            gains_db_per_sample: per-sample applied gain in dB.
        """
        wf = np.asarray(waveform, dtype=float)
        n = len(wf)
        if n == 0:
            return wf, np.array([], dtype=float)

        n_blocks = int(np.ceil(n / block_size))
        gains_db = np.empty(n_blocks, dtype=float)

        for i in range(n_blocks):
            start = i * block_size
            end = min(start + block_size, n)
            blk = wf[start:end]

            # desired instantaneous gain for this block (dB)
            desired_db = self.compute_agc_gain_db(blk, target_vpp, margin_db=margin_db, mode=mode)

            # block duration and smoothing coefficients
            block_time = len(blk) / float(fs)
            tau_a = max(1e-6, attack_ms / 1000.0)
            tau_r = max(1e-6, release_ms / 1000.0)
            alpha_a = 1.0 - np.exp(-block_time / tau_a)
            alpha_r = 1.0 - np.exp(-block_time / tau_r)

            prev = self.gain_db if i == 0 else gains_db[i - 1]
            alpha = alpha_a if desired_db > prev else alpha_r

            gains_db[i] = float((1.0 - alpha) * prev + alpha * desired_db)
            gains_db[i] = float(np.clip(gains_db[i], self.min_gain_db, self.max_gain_db))

        # expand block gains to per-sample gains
        if interp and n_blocks > 1:
            block_centers = (np.arange(n_blocks) * block_size + 0.5 * block_size)[:n_blocks]
            sample_idx = np.arange(n)
            gains_db_per_sample = np.interp(sample_idx, block_centers, gains_db)
        else:
            gains_db_per_sample = np.repeat(gains_db, block_size)[:n]

        # apply per-sample gain and optional noise
        lin_gain = 10.0 ** (gains_db_per_sample / 20.0)
        scaled_waveform = wf * lin_gain
        if self.noise_std > 0.0:
            scaled_waveform = scaled_waveform + np.random.normal(0.0, self.noise_std, size=scaled_waveform.shape)

        # update instance gain to last applied block for continuity
        self.gain_db = float(gains_db[-1])

        return scaled_waveform, gains_db_per_sample