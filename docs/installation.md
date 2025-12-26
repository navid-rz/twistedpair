# Installation

Quick install and running examples locally.

1. Create a virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
# or editable install for development
pip install -e .
```

3. Run a quick example (see `examples/`):

```powershell
python examples\quickstart.py
```

Notes:
- The project uses `requirements.txt` for runtime dependencies and `pyproject.toml` for packaging metadata.
- If tests are present, run them with `pytest`.
