
import numpy as np
from rx.rx import Rx
from config.schema import RxCfg

def test_rx_output_shape():
	cfg = RxCfg(ctle_params={'taps': [1.0]}, slicer_type='NRZ')
	rx = Rx(cfg)
	dummy_waveform = np.ones(160)
	bits = rx.run(dummy_waveform)
	assert isinstance(bits, np.ndarray)
