# Feedback: Lab Topic 1_1

- Lab specification: `LABS/Lab Topic 1_1.pdf`
- Submission folder: `PHYS5394-Miriam`
- Review date: 2026-10-20
- Review method: Static inspection only; student and instructor code were not executed.

## Overview

The Python implementation generates all eight assigned signal types, creates time-domain plots and positive-frequency FFT-magnitude plots, and includes the requested small-step sinusoid comparison. The README provides clear parameter and spectrum explanations. The principal improvements are to demonstrate sampling-rate convergence and to make the one-second sample-grid convention consistent with the lab’s $t_n=n\Delta$ definition.

## Submission identification and files reviewed

The matching submission is in `Lab1/`: `signals.py`, `run.py`, and `README.md`. The folder also contains the specified PDF copy and eight output PNGs; the output images were not treated as independently verified results. The code is in Python, while the lab directs students to add code to the course repository and follow a MATLAB-function example. The signal formulas and analysis are present, but whether the language and repository convention are mandatory is unclear from the PDF; confirm this expectation with the instructor.

## Instructor reference material

- `DATASCIENCE_COURSE/SIGNALS/crcbgenqcsig.m`: reference quadratic-chirp equation and normalization.
- `DATASCIENCE_COURSE/SIGNALS/testcrcbgenqcsig.m`: reference signal sampling and periodogram workflow.

## Lab objectives and requirements

| Requirement | Status | Code evidence and feedback |
|---|---|---|
| Generate the eight specified signal forms (Part 1: signal definitions) | Addressed in code | `signals.py` implements the quadratic chirp, sinusoid, linear chirp, sine-Gaussian, FM, AM, AM-FM, and linear transient chirp. Their formulas appear consistent with the PDF, including the transient time shift. |
| Add code to the course repository and follow the MATLAB function example (Part 1: “Signal generation” and “Format of a Matlab function definition”) | Cannot determine from static inspection | The reviewed implementation uses Python functions. The PDF points to a MATLAB function and the forked course repository, but does not unambiguously state whether Python is disallowed. Confirm the expected language and repository convention; no MATLAB implementation was identified in `Lab1/`. |
| Choose a sufficiently fine sampling interval by reducing it until plots stop changing (Part 1: “Plots”) | Partially addressed | `run.py` chooses 250 Hz from the quadratic chirp’s 25 Hz maximum and uses that grid for all signals, but it does not compare plots at progressively smaller intervals. Add a brief coarse-to-fine comparison to show why the selected interval is adequate. |
| Plot the magnitude of the FFT against positive-frequency values, using spacing $1/(N\Delta)$ (Part 2: “FFT”) | Partially addressed | `positive_periodogram` uses the correct positive-bin count and calculates spacing as `1/(nSamples*samplIntrvl)`. However, `run.py` creates 251 samples from 0 through 1 second at 250 Hz. The grid therefore includes both endpoints rather than following a half-open $t_n=n\Delta$ sequence for a one-second record. Use 250 samples on `[0, 1)` (for example, `np.arange(nSamples)*samplIntrvl`) or explicitly redefine the duration and keep the FFT spacing aligned with that convention. |
| Interpret periodograms, including finite-duration sinusoid behavior and frequency steps below $1/T$ (Part 2: “Frequencies in a DFT”) | Partially addressed | `run.py` compares 6.00, 6.50, 7.00, and 7.50 Hz, with 0.50 Hz steps below 1 Hz for the one-second signal. The README interprets the spectra of all eight signals, but it does not discuss the finite-duration sinusoid’s sinc-like spectrum and calls attention to overlap without explaining the sampling-grid effect on frequency spacing. Add that explanation after correcting the grid. |

## Code correctness and suggested improvements

- **Location:** `run.py`, time-vector construction and frequency comparison. **Observation:** `nSamples = int(1 / samplIntrvl) + 1` followed by `np.linspace(0, 1, nSamples)` includes both endpoints, creating 251 samples at 250 Hz for a nominal one-second record. **Likely consequence:** The FFT has a bin spacing of about 0.996 Hz instead of the 1 Hz spacing associated with a 250-sample, one-second record, and the endpoint duplicates the initial phase for periodic signals. **Suggested improvement:** Use a half-open sample grid with exactly `duration * samplingFrequency` samples, then retain the existing `1/(N*Delta)` frequency calculation. This is clear from inspection; the numerical impact was not independently tested.

No other obvious formula or positive-frequency indexing defect was identified in the reviewed code. This does not establish runtime or numerical correctness.

## Documentation feedback

### What works well

The README explains the project layout, run entry point, signal parameters, sample-rate rationale, frequency spacing, and expected spectral features. Function docstrings describe inputs and outputs, and the code uses readable signal-specific function names.

### Suggested improvements

Align the stated frequency-spacing example with a half-open, one-second sample grid. Add a short note about the sinc-like spectrum of a finite-duration sinusoid and clarify that the plots are generated artifacts rather than independently verified evidence.

## Recommended next steps

1. Use a consistent half-open time grid for the one-second record and update the spacing calculation in the README.
2. Show sampled plots at progressively finer intervals to document the chosen interval.
3. Add an interpretation of the finite-duration sinusoid’s sinc-like spectrum and the sub-$1/T$ comparison.

## Review limitations

Student and instructor code were not executed. Runtime behavior and numerical outputs, including the submitted PNGs, were not independently verified. The assessment uses the official lab PDF in `LABS/`; the PDF copy in `Lab1/` was not substituted as the specification.