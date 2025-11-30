
import numpy as np
from channel.simple import simple_channel, copper_channel
from config.schema import ChannelCfg

def test_simple_channel_pass():
	cfg = ChannelCfg(type='simple', fixed_loss_db=0.0)
	waveform = np.ones(100)
	out = simple_channel(waveform, cfg)
	assert isinstance(out, np.ndarray)
	assert out.shape == waveform.shape

def test_copper_channel_pass():
	cfg = ChannelCfg(type='copper', fixed_loss_db=0.0)
	waveform = np.ones(100)
	out = copper_channel(waveform, cfg)
	assert isinstance(out, np.ndarray)
	assert out.shape == waveform.shape
