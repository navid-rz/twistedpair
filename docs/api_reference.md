# API Reference (Pointers)

This document is a pointer guide to where to find core code and public functions.

- Top-level link composition: `link/link.py` — build and run a simulation.
- Transmitter entrypoints: `tx/tx.py`, `tx/driver.py`.
- Receiver entrypoints: `rx/rx.py`, `rx/cdr.py`, `rx/dfe.py`.
- Channel models: `channel/base.py`, `channel/simple.py`, `channel/sparam.py`.
- Configuration: `config/load.py`, `config/schema.py`.
- Metrics: `metrics/ber.py`, `metrics/eye.py`, `metrics/eq.py`.

For deeper exploration, open the module files and inspect the classes and functions. Docstrings in the source code provide parameter descriptions and expected shapes for arrays and signals.
