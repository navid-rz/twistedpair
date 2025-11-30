import numpy as np
from types import SimpleNamespace
from tx.tx import Tx
from analysis.plots import plot_waveform, plot_psd, plot_eye
from scipy.signal import welch, find_peaks
from channel.simple import copper_channel  # added import

# Build a minimal config that matches the current Tx implementation (cfg.tx.*)
cfg = SimpleNamespace(
    tx=SimpleNamespace(
        data_rate_gbps=25.78125,            # line rate in Gbps
        modulation='NRZ',                   # 'NRZ' or 'PAM4'
        ffe_taps=[1.0],                     # symbol-domain FFE taps
        dac=SimpleNamespace(                # nested DAC params expected by Tx
            sps=4,
            resolution_bits=8,
            v_cm=1.0,
            v_swing=0.8
        ),
        jitter=SimpleNamespace(type='gaussian', stddev=0.0005)
    )
)

# Simulation control (kept simple)
sim = SimpleNamespace(
    n_symbols=500000,
    sps=16,               # simulation samples per symbol (for analysis / sim_sample_rate)
    prbs_order=23,
    random_seed=0x7FFFFFFFF,
    bit_mode='prbs'
)

tx = Tx(cfg)

# Determine symbol rate / sample rate from cfg
data_rate_bps = cfg.tx.data_rate_gbps * 1e9
if cfg.tx.modulation.lower() == 'pam4':
    symbol_rate = data_rate_bps / 2.0
else:
    symbol_rate = data_rate_bps
sample_rate = sim.sps * symbol_rate  # simulation sample rate (samples/second) for PSD/analysis

# Generate bits and run transmitter
tx.generate_bits(
    sim.n_symbols,
    mode=sim.bit_mode,
    seed=sim.random_seed,
    prbs_order=sim.prbs_order
)
print(f"Bit mode: {sim.bit_mode}")

# Debug prints
print("First 10 bits:", tx.bits[:10])

# Run the transmitter and request waveform at simulation sample rate
waveform, time = tx.run(sim_sample_rate=sample_rate)

print("First 10 symbols:", tx.symbols[:10])
print("First 10 symbols after FFE:", tx.symbols_ffe[:10])
print('--- TX STAGES ---')
print('Waveform length:', len(waveform))
print('Time length:', len(time))

# Plot a portion of the waveform (time is in seconds)
plot_waveform(waveform[:5000], time[:5000], title="TX Waveform (25G NRZ)")

# PSD (use simulation sample rate)
plot_psd(waveform, sample_rate, title="TX PSD (25G NRZ)")

# --- Eye diagram calculation and plot ---
# use simulation sps (sim.sps) since waveform was produced at sim_sample_rate
sim_sps = int(sim.sps)
if sim_sps <= 0:
    raise ValueError("sim.sps must be > 0 for eye calculation")

segment_symbols = 2  # number of symbol periods per eye trace (common: 2)
segment_len = sim_sps * segment_symbols

# number of eye traces we can extract (advance by one symbol per trace)
n_traces = max(0, (len(waveform) - segment_len) // sim_sps)
max_traces = 500  # limit to keep plotting reasonable
n_traces = min(n_traces, max_traces)

eye_traces = []
for k in range(n_traces):
    start = k * sim_sps
    seg = waveform[start:start + segment_len]
    if len(seg) == segment_len:
        eye_traces.append(seg)

if eye_traces:
    # pass simulation sample rate so x-axis is actual time
    plot_eye(eye_traces, sim_sample_rate=sample_rate, title=f"Eye Diagram ({segment_symbols}-symbol overlay)")
else:
    print("Not enough samples to build eye diagram.")

# --- Apply copper channel and analyze ---
# simple channel config using SimpleNamespace to match ChannelCfg fields used by channel.simple
channel_cfg = SimpleNamespace(
    alpha_db_per_in_ghz=0.1,   # copper loss coefficient
    length_in=5.0,             # length in inches
    f_ref_ghz=10.0,
    fixed_loss_db=3.0,         # extra fixed loss in dB
    awgn_sigma=0.0005,         # channel AWGN (voltage)
    delay=0,                   # sample delay
    isi_taps=None
)

waveform_chan = copper_channel(waveform, channel_cfg)

# Ensure time array matches channel output length
time_chan = time[:len(waveform_chan)]

# Plot waveform after channel
plot_waveform(waveform_chan[:5000], time_chan[:5000], title="TX Waveform after Copper Channel")

# PSD after channel
plot_psd(waveform_chan, sample_rate, title="TX PSD after Copper Channel")

# Eye diagram after channel
n_traces_chan = max(0, (len(waveform_chan) - segment_len) // sim_sps)
n_traces_chan = min(n_traces_chan, max_traces)

eye_traces_chan = []
for k in range(n_traces_chan):
    start = k * sim_sps
    seg = waveform_chan[start:start + segment_len]
    if len(seg) == segment_len:
        eye_traces_chan.append(seg)

if eye_traces_chan:
    plot_eye(eye_traces_chan, sim_sample_rate=sample_rate, title=f"Eye Diagram (after copper channel, {segment_symbols}-symbol overlay)")
else:
    print("Not enough samples to build post-channel eye diagram.")
