# Modules Reference

Short descriptions of the major modules and where to look for implementation details.

- `tx/` — Transmitter stack
  - `dac.py`, `driver.py`, `ffe.py`, `jitter.py`, `mapping.py`, `synth.py`, `tx.py`
  - Responsible for symbol mapping, pre-emphasis (FFE), jitter injection, and DAC modeling.

- `rx/` — Receiver stack
  - `adc.py`, `cdr.py`, `ctle.py`, `dfe.py`, `nco.py`, `rx.py`, `slicer.py`, `vga.py`
  - Models analog front-end, timing recovery, equalization, and bit decision.

- `channel/` — Channel and S-parameter handling
  - `base.py`, `simple.py`, `sparam.py`
  - Provides simple parametric channels and S-parameter based filtering.

- `link/` — High-level link composition
  - `link.py` composes TX, channel, and RX and manages simulation runs.

- `metrics/` — Analysis metrics
  - `ber.py`, `eq.py`, `eye.py` for BER estimation, equalizer analysis, and eye metrics.

- `examples/` — Scripts demonstrating use cases
  - `quickstart.py`, `tx_demo.py`, `link_demo.py`, `tx_and_channel_demo.py`, etc.

- `config/` & `configs/` — Configuration loader and example presets

For code-level exploration, open the module files in the directories above.
