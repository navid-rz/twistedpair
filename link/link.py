

from typing import Any
from tx.tx import Tx
from rx.rx import Rx
from channel.simple import simple_channel, copper_channel
from config.schema import TxCfg, RxCfg, ChannelCfg

class Link:
	"""
	End-to-end link: Tx → channel → Rx. Configurable via dataclasses.
	Supports 'simple' and 'copper' channel types.
	"""
	def __init__(self, tx_cfg: TxCfg, ch_cfg: ChannelCfg, rx_cfg: RxCfg) -> None:
		"""
		Args:
			tx_cfg: TxCfg dataclass instance.
			ch_cfg: ChannelCfg dataclass instance.
			rx_cfg: RxCfg dataclass instance.
		"""
		self.tx = Tx(tx_cfg)
		self.rx = Rx(rx_cfg)
		self.ch_cfg = ch_cfg

	def run(self) -> Any:
		"""
		Run end-to-end link simulation.
		Returns:
			Rx output bits or symbols.
		"""
		# 0. Generate bits for Tx
		n_symbols = getattr(self.ch_cfg, 'n_symbols', 10000)
		bit_mode = getattr(self.tx.cfg, 'bit_mode', 'random')
		sps = getattr(self.ch_cfg, 'sps', 8)
		self.tx.generate_bits(n_symbols, mode=bit_mode)

		# 1. Generate Tx waveform
		waveform, _ = self.tx.run(sps=sps)
		# 2. Pass through channel
		if self.ch_cfg.type == 'copper':
			ch_waveform = copper_channel(waveform, self.ch_cfg)
		else:
			ch_waveform = simple_channel(waveform, self.ch_cfg)
		# 3. Run Rx
		rx_out = self.rx.run(ch_waveform, sps=sps)
		return rx_out
