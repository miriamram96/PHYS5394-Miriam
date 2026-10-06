"""
Part 1:
For each of the signals generated for Lab 1, find the highest
instantaneous frequency in the signal.

Sample signals at:
- The Nyquist rate (2 x highest frequency)
- 2x Nyquist rate
- 10 x Nyquist rate

The output of this script is on `output/sampling`, with one figure per signal.
Each figure has three rows, one for each sampling rate, and two columns:
the time domain signal and its periodogram.
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# Import the same signal functions used in Lab 1.
from signals import (
    quadratic_chirp,
    sinusoid,
    linear_chirp,
    sine_gaussian,
    fm_sinusoid,
    am_sinusoid,
    am_fm_sinusoid,
    linear_transient_chirp,
)


# Create output folder for the saved plots:
outputFolder = Path(__file__).with_name("output") / "sampling"
outputFolder.mkdir(parents=True, exist_ok=True)


# Lab 1 parameters and maximum frequencies calculated from the phase derivatives.
# The math is explained in the README.
t = 1.0  # Last 'time' in the one second interval.

# Quadratic chirp: f(t) = a1 + 2*a2*t + 3*a3*t**2.
a1, a2, a3 = 10.0, 3.0, 3.0
qcCoefs = [a1, a2, a3]
quadMax = a1 + 2 * a2 * t + 3 * a3 * t**2

# Sinusoid: its frequency stays at f0.
sinusoidF0 = 7.0
sinusoidMax = sinusoidF0

# Linear chirp: f(t) = f0 + f1*t.
linearF0, linearF1 = 2.0, 8.0
linearMax = linearF0 + linearF1 * t

# Sine-Gaussian: use the carrier phase frequency.
gaussianF0 = 15.0
gaussianMax = gaussianF0

# FM: f(t) = f0 - b*f1*sin(2*pi*f1*t).
# The sine reaches -1 and +1 during this interval.
fmF0, fmF1, fmB = 10.0, 2.0, 2.0
fmMax = fmF0 + abs(fmB * fmF1)

# AM: use the carrier phase frequency.
amF0, amF1 = 15.0, 2.0
amMax = amF0

# AM-FM: its phase has the same frequency formula as FM.
amFmF0, amFmF1, amFmB = 15.0, 2.0, 2.0
amFmMax = amFmF0 + abs(amFmB * amFmF1)

# Transient chirp: f(u) = f0 + 2*f1*u, evaluated at the end of its active interval.
transientF0, transientF1, length = 3.0, 6.0, 0.50
transientMax = transientF0 + 2 * transientF1 * length

# The list stores each signal's file name, plot title, and calculated maximum frequency.
signalList = [
    ("quadratic_chirp", "Quadratic Chirp", quadMax),
    ("sinusoid", "Sinusoid", sinusoidMax),
    ("linear_chirp", "Linear Chirp", linearMax),
    ("sine_gaussian", "Sine Gaussian", gaussianMax),
    ("fm_sinusoid", "Frequency Modulated (FM) Sinusoid", fmMax),
    ("am_sinusoid", "Amplitude Modulated (AM) Sinusoid", amMax),
    ("am_fm_sinusoid", "AM-FM Sinusoid", amFmMax),
    ("linear_transient_chirp", "Linear Transient Chirp", transientMax),
]


# Multiply the Nyquist rate by 1, 2, and 10.
rateMultipliers = [1, 2, 10]

# Work through one signal at a time to create 6 plots.
for fileName, title, maxFrequency in signalList:
    fig, axes = plt.subplots(3, 2, figsize=(11, 9))
    nyquistRate = 2 * maxFrequency
    print(f"{title}. Maximum instantaneous frequency = {maxFrequency:g} Hz")

    # Each sampling rate gets one row: Nyquist, 2 x Nyquist, 10 x Nyquist.
    for row, multiplier in enumerate(rateMultipliers):
        samplingFrequency = multiplier * nyquistRate
        samplingInterval = 1 / samplingFrequency

        # Make sample times from 0 to 1 second.
        # Add one sample because the count includes n = 0.
        nSamples = int(samplingFrequency) + 1
        timeSamples = np.arange(nSamples) * samplingInterval

        # Generate only the current signal, using the sample times chosen above.
        if fileName == "quadratic_chirp":
            signalValues = quadratic_chirp(timeSamples, amp=10.0, qcCoefs=qcCoefs)
        elif fileName == "sinusoid":
            signalValues = sinusoid(timeSamples, amp=1.0, f0=sinusoidF0, phi0=0.0)
        elif fileName == "linear_chirp":
            signalValues = linear_chirp(timeSamples, amp=1.0, f0=linearF0, f1=linearF1, phi0=0.0)
        elif fileName == "sine_gaussian":
            signalValues = sine_gaussian(timeSamples, amp=1.0, t0=0.50, sigma=0.10, f0=gaussianF0, phi0=0.0)
        elif fileName == "fm_sinusoid":
            signalValues = fm_sinusoid(timeSamples, amp=1.0, b=fmB, f0=fmF0, f1=fmF1)
        elif fileName == "am_sinusoid":
            signalValues = am_sinusoid(timeSamples, amp=1.0, f0=amF0, f1=amF1, phi0=0.0)
        elif fileName == "am_fm_sinusoid":
            signalValues = am_fm_sinusoid(timeSamples, amp=1.0, b=amFmB, f0=amFmF0, f1=amFmF1)
        elif fileName == "linear_transient_chirp":
            signalValues = linear_transient_chirp(timeSamples, amp=1.0, ta=0.25, f0=transientF0, f1=transientF1, phi0=0.0, length=length)

        # Calculate the FFT magnitude and its zero/positive frequency labels.
        # frequencies is the x-axis and fftMagnitude is the y-axis.
        frequencies = np.fft.rfftfreq(nSamples, d=samplingInterval)
        fftMagnitude = np.abs(np.fft.rfft(signalValues))

        # Plot the sampled signal on the left and its periodogram on the right.
        timeAxis, frequencyAxis = axes[row]
        timeAxis.plot(timeSamples, signalValues, ".-", markersize=3)
        timeAxis.set_title(f"{multiplier} x Nyquist rate: fs = {samplingFrequency:g} Hz")
        timeAxis.set_xlabel("Time (sec)")
        timeAxis.set_ylabel("Amplitude")
        timeAxis.grid(alpha=0.25)

        frequencyAxis.plot(frequencies, fftMagnitude, ".-", markersize=3)
        frequencyAxis.set_title("Periodogram")
        frequencyAxis.set_xlabel("Frequency (Hz)")
        frequencyAxis.set_ylabel("|FFT|")
        frequencyAxis.grid(alpha=0.25)

        # On the terminal:
        # Print the rate, time between samples, and total number of samples.
        print(f"fs = {samplingFrequency:g} Hz, dt = {samplingInterval:.6f} sec, N = {nSamples}")

    fig.suptitle(title)
    fig.tight_layout()
    fig.savefig(outputFolder / f"{fileName}.png", dpi=150)
    plt.close(fig)

print(f"Saved plots to: {outputFolder}")
