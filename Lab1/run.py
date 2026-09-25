"""
Generate the assigned signals, plot each one in the time and frequency
domains, and save the finished figures in the output folder.

Author: Miriam Ramos Arevalo
Date: September 2026
"""

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

# Where signal is the script `signals.py` that contains the signal generating functions.
from signals import (
    am_fm_sinusoid,
    am_sinusoid,
    fm_sinusoid,
    linear_chirp,
    linear_transient_chirp,
    quadratic_chirp,
    sine_gaussian,
    sinusoid)


# 1: Set up the times at which the signals will be calculated.

# The quadratic chirp has the highest frequency (25 Hz at t = 1 second), 
# so it is used to choose a sampling rate that is high enough for every signal.
    # (A detailed exaplanation of this is provived in the README file, 
    # under the "Sampling interval calculation" section.)
maxFreq = 25.0
nyqFreq = 2 * maxFreq
samplingFrequency = 5 * nyqFreq
samplIntrvl = 1 / samplingFrequency

# Include both 0 and 1 second in the sample times.
nSamples = int(1 / samplIntrvl) + 1
timeSamples = np.linspace(0, 1, nSamples)


# 2: Generate each of the signals using the same sample times.

# Call the functions from signals.py and give each one the parameters it needs.
quadChirp = quadratic_chirp(timeSamples, amp=10.0, qcCoefs=[10.0, 3.0, 3.0])
sinusoidSignal = sinusoid(timeSamples, amp=1.0, f0=7.0, phi0=0.0)
linearChirp = linear_chirp(timeSamples, amp=1.0, f0=2.0, f1=8.0, phi0=0.0)
sineGaussian = sine_gaussian(timeSamples, amp=1.0, t0=0.50, sigma=0.10, f0=15.0, phi0=0.0)
fmSinusoid = fm_sinusoid(timeSamples, amp=1.0, b=2.0, f0=10.0, f1=2.0)
amSinusoid = am_sinusoid(timeSamples, amp=1.0, f0=15.0, f1=2.0, phi0=0.0)
amFmSinusoid = am_fm_sinusoid(timeSamples, amp=1.0, b=2.0, f0=15.0, f1=2.0)
transientChirp = linear_transient_chirp(timeSamples, amp=1.0, ta=0.25, f0=3.0, f1=6.0, phi0=0.0, length=0.50)

# Store each signal with the file name and title used for its plot.
signalPlots = [
    ("quadratic_chirp", "Quadratic chirp", quadChirp),
    ("sinusoid", "Sinusoid", sinusoidSignal),
    ("linear_chirp", "Linear chirp", linearChirp),
    ("sine_gaussian", "Sine-Gaussian", sineGaussian),
    ("fm_sinusoid", "Frequency modulated (FM) sinusoid", fmSinusoid),
    ("am_sinusoid", "Amplitude modulated (AM) sinusoid", amSinusoid),
    ("am_fm_sinusoid", "AM-FM sinusoid", amFmSinusoid),
    ("linear_transient_chirp", "Linear transient chirp", transientChirp),
]


# 3: Create a function to calculate the positive frequencies and FFT magnitudes.
def positive_periodogram(signalValues, samplIntrvl):
    """Return the positive frequencies and FFT magnitude of a signal.

    Parameters:
        signalValues: All signal amplitudes (251 values in this lab).
        samplIntrvl: Time between samples (0.004 seconds in this lab).
    Returns:
        posFreq: Positive frequency values (Hz).
        FFTMag: FFT magnitude at each positive frequency.
    """
    nSamples = len(signalValues)

    # The FFT returns positive and negative frequencies. 
    # We have to plot only zero and the positive frequencies.
    # // is integer division.
    numPosFreq = nSamples // 2
    
    # Add one to include zero frequency.
    numPosFreq = numPosFreq + 1
    
    # Frequency spacing = 1/(N*Delta), where N is the number of samples and
    # Delta is the sampling interval. 
    freqSpacing = 1 / (nSamples * samplIntrvl)
    
    # posFreq contains the frequencies used along the periodograms x-axis.
    posFreq = np.arange(numPosFreq) * freqSpacing

    # Calculate the FFT. 
    # The result contains complex numbers with real and imaginary parts.
    FFTVal = np.fft.fft(signalValues)

    # [:numPosFreq] keeps the first FFT values: zero and positive frequencies.
    # np.abs() gives the magnitude of each complex FFT value.
    # This will become the y-axis of the periodogram.
    FFTMag = np.abs(FFTVal[:numPosFreq])
    
    return posFreq, FFTMag


# 4: Set up the output folder.
# Put all generated figures in one output directory.
outputFolder = Path(__file__).with_name("output")
outputFolder.mkdir(exist_ok=True)


# 5: Set up the extra sinusoid comparison.
# Frequency spacing used before: 1/(N*Delta).
freqSpacing = 1 / (nSamples * samplIntrvl)

# Set up 4 frequencies around 7 Hz, separated by 0.50 Hz.
# The 0.50 Hz steps are smaller than 1/T = 1 Hz for this one second signal.
smallStepFreqs = [6.00, 6.50, 7.00, 7.50]


# 6: Plot each signal and save output.
outputFiles = []

for fileName, title, signalValues in signalPlots:
    # The sinusoid needs a third plot for its frequency comparison.
    nRows = 3 if fileName == "sinusoid" else 2
    figureHeight = 12 if nRows == 3 else 8
    signalFig, axes = plt.subplots(nRows, 1, figsize=(9, figureHeight))

    # Use the first row for time and the second row for frequency.
    timeAxis = axes[0]
    frequencyAxis = axes[1]

    # The top plot is the time domain: the signals value at each moment.
    timeAxis.plot(timeSamples, signalValues, linewidth=1.2)
    timeAxis.set_title("Time Domain")
    timeAxis.set_xlabel("Time (sec)")
    timeAxis.set_ylabel("Amplitude")
    timeAxis.grid(alpha=0.25)

    # The bottom plot is the periodogram: the FFT magnitude at each frequency.
    posFreq, FFTMag = positive_periodogram(signalValues, samplIntrvl)
    frequencyAxis.plot(posFreq, FFTMag, linewidth=1.2)
    frequencyAxis.set_title("Periodogram")
    frequencyAxis.set_xlabel("Frequency (Hz)")
    frequencyAxis.set_ylabel("|FFT|")
    frequencyAxis.set_xlim(0, 30)
    frequencyAxis.grid(alpha=0.25)

    # This is the sinusoid frequency comparison from Slide 14.
    if fileName == "sinusoid":
        comparisonAxis = axes[2]
        for f0 in smallStepFreqs:
            stepSignal = sinusoid(timeSamples, amp=1.0, f0=f0, phi0=0.0)
            stepFreq, stepFFTMag = positive_periodogram(stepSignal, samplIntrvl)
            comparisonAxis.plot(stepFreq, stepFFTMag,marker="o", markersize=3, linewidth=1.1, label=f"f0 = {f0:.2f} Hz")

        comparisonAxis.set_xlim(0, 15)
        comparisonAxis.set_xlabel("Frequency (Hz)")
        comparisonAxis.set_ylabel("|FFT|")
        comparisonAxis.set_title("Slide 14: Sinusoid Frequency Comparison")
        comparisonAxis.grid(alpha=0.25)
        comparisonAxis.legend()

    signalFig.suptitle(title, fontsize=16)
    signalFig.tight_layout(rect=[0, 0, 1, 0.99])

    # Save the figure:
    outputFile = outputFolder / f"{fileName}.png"
    signalFig.savefig(outputFile, dpi=200)
    outputFiles.append(outputFile)


# 7: Print the sampling information and show the figures.
print(f"Sampling frequency: {samplingFrequency:.0f} Hz")
print(f"Sampling interval: {samplIntrvl:.4f} seconds")
print(f"Number of samples: {nSamples}")
print(f"Frequency spacing: {freqSpacing:.4f} Hz")
print(f"Saved {len(outputFiles)} signal result files to: {outputFolder}")

plt.show()
