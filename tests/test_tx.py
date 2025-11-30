
import numpy as np
from tx.tx import Tx
from config.schema import TxCfg

def test_tx_waveform_shape():
	cfg = TxCfg(data_rate=1.0, modulation='NRZ', prbs_order=7)
	tx = Tx(cfg)
	waveform, time = tx.run()
	assert isinstance(waveform, np.ndarray)
	assert len(waveform) == len(time)
