# HolidayLights — Python port

This folder contains a Python port of the Arduino HolidayLights sketch.

Contents
- `holidaylights/` — Python package with core classes and adapters
- `run_mock.py` — Demo that runs on any platform using the mock adapter
- `run_rpi.py` — Example to run on Raspberry Pi using `rpi_ws281x` (requires hardware)
- `run_circuitpython.py` — Example usage for CircuitPython boards

Quick start (mock)

1. Create and activate a virtual environment (recommended)

  - Windows PowerShell:
    - `python -m venv .venv`
    - `.\.venv\Scripts\Activate.ps1`

  - Windows CMD:
    - `python -m venv .venv`
    - `.\.venv\Scripts\activate.bat`

  - macOS / Linux (bash / zsh):
    - `python3 -m venv .venv`
    - `source .venv/bin/activate`

  - To deactivate the environment (all platforms):
    - `deactivate`

  - Optional: upgrade pip inside the venv before installing packages:
    - `python -m pip install --upgrade pip`

  Notes: Using a virtual environment keeps dependencies local to the project and is the recommended way to install both third-party and local Python libraries. To install a local package in editable mode (useful during development), run `pip install -e .` from the package root if you have a `pyproject.toml` or `setup.py` present.

2. Install dependencies (only what you need):
  - `pip install -r ../requirements.txt`

3. Run the mock demo:
  - `python run_mock.py`

Raspberry Pi (rpi_ws281x)
- Install `rpi_ws281x` (may require system packages and running as root depending on your setup):
  - `pip install rpi_ws281x`
- Edit `run_rpi.py` for your GPIO pin configuration if necessary, then run on the Pi:
  - `python run_rpi.py`

CircuitPython (Adafruit)
- On CircuitPython boards use `adafruit-circuitpython-neopixel`.
- On single-board computers you can use Adafruit Blinka to access CircuitPython libraries:
  - `pip install Adafruit-Blinka adafruit-circuitpython-neopixel`
- `run_circuitpython.py` is a small example showing how to use the `CircuitPythonAdapter`.

Testing
- Tests are under `python/tests` and use `pytest`.
  - From the repo root: `pip install -r requirements.txt && pytest python/tests`

Notes & troubleshooting
- The Raspberry Pi adapter requires appropriate permissions to access PWM/GPIO. Run with `sudo` if needed.
- The mock adapter prints compact frames to the console for development and unit testing.

Feel free to open an issue or request a feature if you'd like additional helpers (PNG export, GUI preview, etc.).
