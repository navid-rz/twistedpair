
import numpy as np
from typing import Sequence, Optional, Tuple, Any
from .ctle import ctle_fir
from .cdr import ideal_sampler
from .dfe import apply_dfe
from .slicer import slicer_nrz, slicer_pam4


from config.schema import RxCfg

class Rx:
	"""
	Receiver pipeline: CTLE → CDR → slicer → DFE.
	Uses RxCfg dataclass for configuration.
	"""
	def __init__(self, cfg: RxCfg) -> None:
		"""
		Args:
			cfg: RxCfg dataclass instance.
		"""
		self.cfg = cfg

	def run(self, waveform: Sequence[float], sps: int = 1, threshold: Optional[float] = None) -> Any:
		"""
		Run the Rx pipeline on input waveform.
		Args:
			waveform: Input waveform samples.
			sps: Samples per symbol.
			threshold: Slicer threshold (midpoint voltage, optional).
		Returns:
			Sliced bits (NRZ) or tuples (PAM4).
		"""
		# 1. CTLE equalization
		ctle_taps = self.cfg.ctle_params.get('taps', [1.0]) if self.cfg.ctle_params else [1.0]
		self.eq_waveform = ctle_fir(waveform, ctle_taps)

		# 2. CDR (sample at symbol rate)
		self.symbols = ideal_sampler(self.eq_waveform, sps)

		# 3. DFE equalization (optional)
		if self.cfg.dfe_taps:
			self.dfe_symbols = apply_dfe(self.symbols, self.cfg.dfe_taps)
		else:
			self.dfe_symbols = self.symbols

		# 4. Slicer (NRZ or PAM4)
		if self.cfg.slicer_type.lower() == 'pam4':
			self.bits = slicer_pam4(self.dfe_symbols, threshold=threshold)
		else:
			self.bits = slicer_nrz(self.dfe_symbols, threshold=threshold)
		return self.bits
	
