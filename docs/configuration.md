# Configuration and Presets

Configuration in `twistedpair` is typically done via YAML preset files in the `configs/` directory.

Key points:
- Use `config/load.py` to load and validate presets via `config/schema.py`.
- Presets specify TX/RX parameters, channel choices, and simulation settings (like symbol rate, sample rate, FFE taps).
- Example preset: `configs/preset_25g_nrz.yaml`.

Workflow:
1. Copy or edit a preset in `configs/`.
2. Load it programmatically in a script via `from config.load import load_preset` (see `examples/`).
