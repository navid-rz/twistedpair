# Usage

Common tasks and example commands.

Run a quick demo:

```powershell
python examples\quickstart.py
```

Run a transmitter-only demo:

```powershell
python examples\tx_demo.py
```

Run a full link demo (TX -> channel -> RX):

```powershell
python examples\link_demo.py
```

Change configuration by editing YAML presets in `configs/` and loading them via `config/load.py`.

For plotting and metrics, inspect `analysis/plots.py` and `metrics/`.
