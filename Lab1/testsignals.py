"""
Generate and plot all signals assigned in Lab 1.

This script sets the sampling information and signal parameters, creates a
shared array of time samples, and calls the functions in signals.py to generate
the 8 assigned signals. 
It plots the signals in one figure and saves the figure as part1_signals.png.

Author: Miriam Ramos Arevalo
Date: September 2026
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from signals import (
    am_fm_sinusoid,
    am_sinusoid,
    fm_sinusoid,
    linear_chirp,
    linear_transient_chirp,
    quadratic_chirp,
    sine_gaussian,
    sinusoid)


# Defining signal parameters: 
a1 = 10.0  
a2 = 3.0  
a3 = 3.0  
A = 10.0  # Signal amplitude

# Instantaneous frequency after 1 sec is:
maxFreq = a1 + 2 * a2 + 3 * a3

# The Nyquist frequency guess: 2 * maximum instantaneous frequency:
nyqFreq = 2 * maxFreq

# Sampling frequency:
samplFreq = 5 * nyqFreq

# Sampling interval:
samplIntrvl = 1 / samplFreq

# One second has 1/0.004 = 250 intervals. Including time 0 gives 251 points.
nSamples = int(1 / samplIntrvl) + 1
# Create 251 evenly spaced time values from 0 to 1 second.
timeSamples = np.linspace(0, 1, nSamples)


# Generate the signals: 
quadChirp = quadratic_chirp(timeSamples, amp=A, qcCoefs=[a1, a2, a3])

sinusoidSignal = sinusoid(timeSamples, amp=1.0, f0=5.0, phi0=0.0)

linearChirp = linear_chirp(
    timeSamples, amp=1.0, f0=2.0, f1=8.0, phi0=0.0)

sineGaussian = sine_gaussian(
    timeSamples, amp=1.0, t0=0.50, sigma=0.10, f0=15.0, phi0=0.0)

fmSinusoid = fm_sinusoid(timeSamples, amp=1.0, b=2.0, f0=10.0, f1=2.0)

amSinusoid = am_sinusoid(
    timeSamples, amp=1.0, f0=15.0, f1=2.0, phi0=0.0)

amFmSinusoid = am_fm_sinusoid(
    timeSamples, amp=1.0, b=2.0, f0=15.0, f1=2.0)

transientChirp = linear_transient_chirp(
    timeSamples,
    amp=1.0,
    ta=0.25,
    f0=3.0,
    f1=6.0,
    phi0=0.0,
    length=0.50)


# Plot the signals: 
signalPlots = [
    ("Quadratic chirp", quadChirp),
    ("Sinusoid", sinusoidSignal),
    ("Linear chirp", linearChirp),
    ("Sine-Gaussian", sineGaussian),
    ("Frequency modulated (FM) sinusoid", fmSinusoid),
    ("Amplitude modulated (AM) sinusoid", amSinusoid),
    ("AM-FM sinusoid", amFmSinusoid),
    ("Linear transient chirp", transientChirp),
]

fig, axes = plt.subplots(4, 2, figsize=(12, 12), sharex=True)

for axis, (title, sigVec) in zip(axes.flat, signalPlots):
    axis.plot(timeSamples, sigVec, linewidth=1.2)
    axis.set_title(title)
    axis.set_ylabel("Amplitude")
    axis.grid(alpha=0.25)

for axis in axes[-1, :]:
    axis.set_xlabel("Time (sec)")

fig.suptitle("Lab 1: Discrete Time Signals", fontsize=16)
fig.tight_layout()

outputFile = Path(__file__).with_name("part1_signals.png")
fig.savefig(outputFile, dpi=200)

print(f"Sampling frequency: {samplFreq:.0f} Hz")
print(f"Sampling interval: {samplIntrvl:.4f} seconds")
print(f"Number of samples: {nSamples}")
print(f"Plot saved to: {outputFile}")

plt.show()
