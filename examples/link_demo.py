"""
Quickstart demo: Run Tx → Channel → Rx using a YAML config file, plot and save results.
"""
import sys
import os
import numpy as np
from config.load import load_main_cfg
from config.schema import TxCfg, RxCfg, SimCfg, ChannelCfg
from tx.tx import Tx
from rx.rx import Rx
from channel.simple import simple_channel, copper_channel
from analysis.plots import plot_waveform, plot_eye, plot_symbols_streams, plot_psd
from metrics.eye import fold_to_eye
from metrics.ber import empirical_ber

def main(cfg_path: str):
	main_cfg = load_main_cfg(cfg_path)
	link_cfg = main_cfg.link
	tx_cfg = link_cfg.tx
	rx_cfg = link_cfg.rx
	sim_cfg = link_cfg.sim
	ch_cfg = link_cfg.channel

	# TX
	tx = Tx(tx_cfg)
	tx.generate_bits(sim_cfg.n_symbols, mode=sim_cfg.bit_mode, seed=sim_cfg.random_seed, prbs_order=sim_cfg.prbs_order)
	waveform, _ = tx.run(sps=sim_cfg.sps)

	# Channel
	if ch_cfg.type == 'copper':
		ch_waveform = copper_channel(waveform, ch_cfg)
	else:
		ch_waveform = simple_channel(waveform, ch_cfg)

	# Calculate slicer threshold (midpoint, e.g. Vcm)
	threshold = getattr(tx_cfg, 'vcm', 0.0)

	# RX
	rx = Rx(rx_cfg)
	rx_out = rx.run(ch_waveform, sps=sim_cfg.sps, threshold=threshold)

	# Ensure output directory exists
	os.makedirs("plots", exist_ok=True)

	# Generate and save plots
	plot_waveform(waveform, None, title="Tx Waveform", save_path="plots/tx_waveform.png")


	# Plot waveform after channel
	plot_waveform(ch_waveform, None, title="Waveform After Channel", save_path="plots/ch_waveform.png")

	# Plot RX CTLE equalized waveform
	plot_waveform(rx.eq_waveform, None, title="RX CTLE Waveform", save_path="plots/rx_ctle_waveform.png")

	# PSD plots (after all other plots)
	sample_rate = sim_cfg.sps * tx.symbol_rate  # Hz
	plot_psd(waveform, sample_rate, title="TX Waveform PSD", save_path="plots/tx_psd.png")
	plot_psd(ch_waveform, sample_rate, title="Channel Output PSD", save_path="plots/ch_psd.png")
	plot_psd(rx.eq_waveform, sample_rate, title="RX CTLE Waveform PSD", save_path="plots/rx_ctle_psd.png")

	plot_symbols_streams(
		[tx.symbols, rx.symbols, rx.dfe_symbols],
		["TX symbols", "RX symbols", "RX DFE symbols"],
		title="TX/RX Symbol Streams",
		save_path="plots/symbol_streams.png"
	)

	# Eye diagram
	eye = fold_to_eye(waveform, sim_cfg.sps)
	plot_eye(eye, title="Tx Eye Diagram", save_path="plots/tx_eye.png")

	# Compute tx_bits and rx_bits
	tx_bits = tx.bits.astype(int)
	rx_bits = np.array(rx_out).astype(int)

	# Print first 10 bits, first 10 tx symbols before FFE, and first 10 after FFE
	print("First 10 bits:", tx_bits[:10])
	print("First 10 Tx symbols (before FFE):", tx.symbols[:10])
	print("First 10 Tx symbols (after FFE):", tx.symbols_ffe[:10])
	print("First 10 Rx bits:", rx_bits[:10])

	# BER computation
	ber = empirical_ber(rx_bits, tx_bits)
	print(f"BER: {ber:.3e}")

	print(f"Demo complete. Plots saved in 'plots/' folder. Config used: {cfg_path}")

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("Usage: python quickstart.py <config.yaml>")
	else:
		main(sys.argv[1])
