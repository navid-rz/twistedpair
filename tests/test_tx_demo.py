import numpy as np
from config.schema import TxCfg, SimCfg
from tx.tx import Tx

def test_tx_short_signal():
    cfg = TxCfg(
        data_rate=25e9,  # 25 Gbps
        prbs_order=3,
        modulation='nrz',
        ffe_taps=[1.0],
        swing=1.0,
        vcm=0.0
    )
    sim = SimCfg(
        n_symbols=4,
        sps=16
    )
    symbol_duration = 1 / cfg.data_rate  # 25G: 40 ps
    tx = Tx(cfg)
    waveform, time = tx.run(n_symbols=sim.n_symbols, sps=sim.sps, symbol_duration=symbol_duration)
    print('--- TX TEST STAGES ---')
    print('Waveform:', waveform)
    print('Time:', time)

if __name__ == "__main__":
    test_tx_short_signal()
