$ErrorActionPreference = "Stop"
. .\.venv\Scripts\Activate.ps1
python --version
python -m pytest -q
