"""
Run Lab 2:
In the terminal write:
    python3 run.py
"""

from pathlib import Path
import runpy

scriptFolder = Path(__file__).resolve().parent

# Part 1: Nyquist sampling comparisons.
runpy.run_path(str(scriptFolder / "sampling.py"), run_name="__main__")

# Part 2: filters the input signal containing three sinusoids.
runpy.run_path(str(scriptFolder / "filtering.py"), run_name="__main__")

# Part 3: generate the signals and calculate their spectrograms.
runpy.run_path(str(scriptFolder / "spectrograms.py"), run_name="__main__")
