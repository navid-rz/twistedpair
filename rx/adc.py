import numpy as np
from typing import Tuple, Optional, Sequence, Union


class ADC:
    """
    Differential ADC model.

    - Input can be (Vp, Vn) pair, 2xN array, or 1D array (treated as single-ended about v_cm).
    - Quantization is performed on the differential waveform (Vp - Vn).
    - By default process() returns the quantized differential voltage array and the ADC sample rate.
      If return_codes=True it returns the integer codes instead.
    """

    def __init__(
        self,
        sps: int,
        resolution_bits: int = 6,
        v_swing: float = 2.0,         # differential Vpp
        v_cm: float = 1.0,
        thermal_noise_stddev: float = 0.0,
    ) -> None:
        if sps < 1:
            raise ValueError("ADC sps must be >= 1")
        self.sps = int(sps)
        self.resolution_bits = int(resolution_bits)
        self.v_swing = float(v_swing)
        self.v_cm = float(v_cm)
        self.thermal_noise_stddev = float(thermal_noise_stddev)

        self.levels = 2 ** self.resolution_bits
        self.v_diff_min = -self.v_swing / 2.0
        self.v_diff_max = +self.v_swing / 2.0

    def _unpack_input(
        self, waveform: Union[Sequence[float], np.ndarray, Tuple[np.ndarray, np.ndarray]]
    ) -> Tuple[np.ndarray, np.ndarray]:
        if isinstance(waveform, (list, tuple)) and len(waveform) == 2:
            vp = np.asarray(waveform[0], dtype=float)
            vn = np.asarray(waveform[1], dtype=float)
            return vp, vn

        arr = np.asarray(waveform)
        if arr.ndim == 2 and arr.shape[0] == 2:
            return arr[0, :].astype(float), arr[1, :].astype(float)
        if arr.ndim == 2 and arr.shape[1] == 2:
            return arr[:, 0].astype(float), arr[:, 1].astype(float)

        if arr.ndim == 1:
            vp = arr.astype(float)
            vn = np.full_like(vp, self.v_cm)
            return vp, vn

        raise ValueError("Unsupported waveform shape for ADC input")

    def process(
        self,
        waveform: Union[Sequence[float], np.ndarray, Tuple[np.ndarray, np.ndarray]],
        sim_sample_rate: float,
        symbol_rate: float,
        add_noise: Optional[bool] = True,
        return_codes: bool = False,
    ) -> Tuple[np.ndarray, float]:
        """
        Process input waveform and return quantized differential waveform (vdiff_q) and adc_fs,
        or integer codes if return_codes=True.
        """
        vp_in, vn_in = self._unpack_input(waveform)

        if sim_sample_rate <= 0 or symbol_rate <= 0:
            raise ValueError("sim_sample_rate and symbol_rate must be > 0")

        # align lengths if necessary
        if vp_in.shape != vn_in.shape:
            n = max(vp_in.size, vn_in.size)
            if vp_in.size != n:
                vp = np.interp(np.linspace(0, 1, n), np.linspace(0, 1, vp_in.size), vp_in)
            else:
                vp = vp_in
            if vn_in.size != n:
                vn = np.interp(np.linspace(0, 1, n), np.linspace(0, 1, vn_in.size), vn_in)
            else:
                vn = vn_in
            vp_in, vn_in = vp, vn

        vp_in = np.asarray(vp_in, dtype=float)
        vn_in = np.asarray(vn_in, dtype=float)

        adc_fs = float(self.sps) * float(symbol_rate)

        # time axes
        t_in = np.arange(len(vp_in)) / float(sim_sample_rate)
        t_end = t_in[-1] if len(t_in) > 0 else 0.0
        if t_end <= 0.0:
            if return_codes:
                return np.array([], dtype=int), adc_fs
            return np.array([], dtype=float), adc_fs

        n_adc = int(np.floor(t_end * adc_fs)) + 1
        t_adc = np.arange(n_adc) / adc_fs
        t_adc_clipped = np.clip(t_adc, t_in[0], t_in[-1])

        # differential waveform interpolation
        vdiff_in = vp_in - vn_in
        vdiff_adc = np.interp(t_adc_clipped, t_in, vdiff_in)

        if add_noise and self.thermal_noise_stddev > 0.0:
            vdiff_adc = vdiff_adc + np.random.normal(0.0, self.thermal_noise_stddev, size=vdiff_adc.shape)

        # clip & quantize differential
        vdiff_clipped = np.clip(vdiff_adc, self.v_diff_min, self.v_diff_max)
        codes = np.round((vdiff_clipped - self.v_diff_min) / (self.v_diff_max - self.v_diff_min) * (self.levels - 1))
        codes = np.clip(codes, 0, self.levels - 1).astype(int)
        vdiff_q = (codes / (self.levels - 1)) * (self.v_diff_max - self.v_diff_min) + self.v_diff_min

        if return_codes:
            return codes, adc_fs

        return vdiff_q, adc_fs