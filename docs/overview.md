# Overview

`twistedpair` is a simulation toolkit for modeling high-speed serial links (SerDes), channels, and transceiver subsystems in Python. It focuses on modular, component-level simulation of transmitters, channels, and receivers, and provides utilities for metrics (BER, eye, equalization), plotting, and example demonstrations.

Key goals:
- Reproducible simulation of TX/RX + channel interactions
- Modular components for rapid experimentation (FFE, CTLE, DFE, CDR, ADC/DAC)
- Scripted examples and presets for common link configs
- Lightweight, dependency-minimal Python implementation

Primary locations in the repository:
- `tx/` — transmitter building blocks and drivers
- `rx/` — receiver chain components
- `channel/` — channel models and S-parameter handling
- `link/` — top-level link composition
- `examples/` — runnable demos and quickstarts
