import numpy as np
from bit_utils.core import prbs, random_bits
from .mapping import map_nrz, map_pam4
from .ffe import apply_ffe, normalize_taps
from .synth import synthesize_waveform
from typing import Tuple
from .dac import DAC

from config.schema import TxCfg

class Tx:
    """
    Transmitter pipeline: PRBS → mapping → FFE → waveform synthesis.
    Uses TxCfg dataclass for configuration.
    """
    def __init__(self, cfg: TxCfg) -> None:
        """
        Args:
            cfg: TxCfg dataclass instance.
        """
        self.cfg = cfg
        self.bits = None

    def generate_bits(self, n_bits: int, mode: str = 'random', seed: int = None, prbs_order: int = 7) -> None:
        """
        Generate bit sequence using random or PRBS mode and store as self.bits.
        Args:
            n_bits: Number of bits to generate
            mode: 'random' or 'prbs'
            seed: Optional seed for reproducibility
            prbs_order: PRBS order (used if mode is 'prbs')
        """
        if mode == 'random':
            bits = random_bits(n_bits, seed=seed)
        elif mode == 'prbs':
            bits = prbs(prbs_order, n_bits, seed=seed)
        else:
            raise ValueError("mode must be 'random' or 'prbs'")
        self.bits = bits

    def run(self, sim_sample_rate: int = 16e9) -> Tuple[np.ndarray, np.ndarray]:
        """
        Run the Tx pipeline and return waveform and time arrays.
        Returns:
            waveform: Synthesized output waveform samples.
            time: Corresponding time array.
        """
        if self.bits is None:
            raise RuntimeError("Bits not generated. Call generate_bits() before run().")

        # Symbol mapping
        data_rate = float(self.cfg.tx.data_rate_gbps) * 1e9  # Gbps -> bps
        if self.cfg.tx.modulation.lower() == 'pam4':
            symbols = map_pam4(self.bits)
            symbol_rate = data_rate / 2.0
        else:
            symbols = map_nrz(self.bits)
            symbol_rate = data_rate

        # FFE (symbol-domain)
        taps = normalize_taps(self.cfg.tx.ffe_taps)
        symbols_ffe = apply_ffe(symbols, taps)

        # DAC configuration (from self.cfg.tx.dac in YAML)
        dac_cfg = self.cfg.tx.dac
        dac = DAC(
            sps=int(dac_cfg.sps),
            resolution_bits=int(dac_cfg.resolution_bits),
            v_cm=float(dac_cfg.v_cm),
            v_swing=float(dac_cfg.v_swing),
        )

        # Synthesize waveform using DAC instance
        waveform, time = synthesize_waveform(
            symbols_ffe,
            dac,
            symbol_rate,
            sim_sample_rate=sim_sample_rate,
            jitter=None
        )
        
        # Store for debugging/inspection
        self.symbols = symbols
        self.symbols_ffe = symbols_ffe
        self.waveform = waveform
        self.time = time
        
        return waveform, time