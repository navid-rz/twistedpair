# Architecture

This section summarizes the core architectural ideas and signal flow used throughout the project.

1. Componentized TX/RX
- Transmitter (`tx/`) components produce discrete-time analog or digital signals. Examples: DAC, FFE, jitter models, mapping.
- Receiver (`rx/`) components process sampled data: CTLE, VGA, ADC, CDR, DFE, slicer.

2. Channel modeling
- Channel models live in `channel/` and accept input waveforms, applying linear (S-parameter) and non-linear impairments. The `sparam.py` module helps load and apply S-parameters.

3. Link composition
- Top-level `link/link.py` composes TX, channel, and RX into a simulation run with configurable parameters.

4. Metrics and analysis
- `metrics/` contains BER, equalizer metrics, and eye-analysis tools. `analysis/plots.py` provides visualization helpers.

5. Configuration & presets
- YAML presets are provided in `configs/`. Use `config/load.py` and `config/schema.py` to validate and load settings.

Typical data flow:
TX -> Channel (impairments) -> RX analog chain -> ADC -> Digital equalization -> Metrics
