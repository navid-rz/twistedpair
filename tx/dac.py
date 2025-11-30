import numpy as np
from typing import Sequence


class DAC:
    """
    Digital-to-Analog Converter (DAC) for the Tx module.
    Converts digital symbols to analog voltages based on the DAC parameters.
    """

    def __init__(self, sps: int, resolution_bits: int, v_cm: float, v_swing: float):
        """
        Initialize the DAC with the given parameters.

        Args:
            sps: Samples per symbol (oversampling ratio).
            resolution_bits: DAC resolution in bits (e.g., 8 for 256 levels).
            v_cm: Common-mode voltage (V).
            v_swing: Maximum differential swing (Vpp).
        """
        self.sps = sps
        self.resolution_bits = resolution_bits
        self.v_cm = v_cm
        self.v_swing = v_swing
        self.quantization_levels = 2**resolution_bits  # Total number of quantization levels
        self.lsb = v_swing / self.quantization_levels  # Voltage step size (LSB)

    def quantize(self, symbols: Sequence[float]) -> np.ndarray:
        """
        Quantize the input symbols to the DAC's resolution.

        Args:
            symbols: Input symbols (e.g., NRZ or PAM4 levels).

        Returns:
            Quantized symbols (float values).
        """
        # Normalize symbols to the range [0, v_swing]
        normalized_symbols = (symbols - (self.v_cm - self.v_swing / 2)) / self.v_swing

        # Scale to quantization levels and round to nearest integer
        quantized_codes = np.clip(
            np.round(normalized_symbols * (self.quantization_levels - 1)),
            0,
            self.quantization_levels - 1,
        )

        # Convert quantized codes back to voltage levels
        quantized_symbols = (
            quantized_codes / (self.quantization_levels - 1) * self.v_swing
            + (self.v_cm - self.v_swing / 2)
        )

        return quantized_symbols

    def upsample(self, quantized_symbols: Sequence[float]) -> np.ndarray:
        """
        Upsample the quantized symbols to the DAC's sampling rate.

        Args:
            quantized_symbols: Quantized symbols (e.g., NRZ or PAM4 levels).

        Returns:
            Upsampled waveform (float values).
        """
        return np.repeat(quantized_symbols, self.sps)

    def process(self, symbols: Sequence[float]) -> np.ndarray:
        """
        Process the input symbols through the DAC.

        Args:
            symbols: Input symbols (e.g., NRZ or PAM4 levels).

        Returns:
            Analog waveform (float values).
        """
        # Quantize the symbols first
        quantized_symbols = self.quantize(symbols)

        # Upsample the quantized symbols
        analog_waveform = self.upsample(quantized_symbols)

        return analog_waveform