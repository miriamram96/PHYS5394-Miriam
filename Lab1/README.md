# Lab 1 - Part 1: Discrete-Time Signal Generation

**Author:** Miriam Ramos Arevalo  
**Date:** September 2026

This folder contains the solution for Lab 1 using Python.
<!-- # TODO: Do Part 2: FT -->

## Files in this directory
- `signals.py`: contains one function for each signal listed in the slides.
- `testsignals.py`: sets the signal parameters, generates every signal, and
  plots the results.
- `part1_signals.png` is produced when `testsignals.py` is run.
- `Lab Topic 1_1.pdf` is the PDF assignment as provided to us in Teams.

## How to run the code?
From this directory, run:
```bash
python3 testsignals.py
```
The code requires NumPy and Matplotlib.

## Signals generated

The script generates all eight signals described in Lab 1:

1. Quadratic chirp signal
2. Sinusoid signal
3. Linear chirp signal
4. Sine-Gaussian signal
5. Frequency-modulated (FM) sinusoid
6. Amplitude-modulated (AM) sinusoid
7. AM-FM sinusoid
8. Linear transient chirp signal

## Variables used in multiple functions

- `dataX`: name used in the provided MATLAB example for the array of times at
  which the signal is evaluated. In this Python code, the same array is named
  `timeSamples` to make its purpose clearer. Each value is measured in seconds.
- `sigVec`: array containing the generated signal values. Each value in
  `sigVec` corresponds to the time at the same position in `timeSamples`.
- `f0`: main frequency of a sinusoid, measured in hertz (Hz). For a chirp, it
  is the frequency at which the chirp starts.
- `f1`: controls how the frequency changes. For a linear chirp, it is the rate
  of frequency change in Hz/sec. For AM and FM signals, it is the modulation
  frequency in Hz.
- `phi0`: starting phase of the signal, measured in radians. It determines
  where in its cycle the sine wave begins at time zero.
- `amp`: amplitude of the signal, which controls the height of the wave.
- `phaseVec`: phase of the signal at each sample time.
- `envelope`: shape applied to the amplitude of a signal.
- `b`: amount of frequency modulation (rad).

## Sampling interval calculation

The MATLAB code uses the following quadratic chirp equations:

```text
signal(t) = A*sin(2*pi*phase(t))
phase(t) = a1*t + a2*t^2 + a3*t^3
frequency(t) = a1 + 2*a2*t + 3*a3*t^2
```

Using the values from **DATASCIENCE_COURSE/SIGNALS/testcrcbgenqcsig.m**:

1. The quadratic chirp uses `a1=10`, `a2=3`, and `a3=3` for a signal that is
   1 second long.
2. The instantaneous frequency equation is:
   `frequency(t) = a1 + 2*a2*t + 3*a3*t^2`.
3. At 1 second, the maximum instantaneous frequency is:
   `maxFreq = 10 + 2(3)(1) + 3(3)(1)^2 = 25 Hz`.
4. Following the MATLAB code, the Nyquist frequency guess is twice the maximum
   instantaneous frequency:
   `nyqFreq = 2*maxFreq = 2(25) = 50 Hz`.
5. The sampling frequency is five times `nyqFreq`:
   `samplFreq = 5*nyqFreq = 5(50) = 250 Hz`.
6. The sampling interval is the inverse of the sampling frequency:
   `samplIntrvl = 1/samplFreq = 1/250 = 0.004 seconds`.

Therefore, the code takes one sample every <u>0.004 seconds</u>.

## MATLAB References:

The quadratic chirp numbers and sampling setup come from these provided MATLAB
files:

- DATASCIENCE_COURSE/SIGNALS/signals.mlx
- DATASCIENCE_COURSE/SIGNALS/testcrcbgenqcsig.m
- DATASCIENCE_COURSE/SIGNALS/crcbgenqcsig.m
