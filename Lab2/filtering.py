"""
Part 2:
Separate 3 sinusoids using FIR filters.

The output of this script is on `output/filtering`, with one figure.
The figure has four rows: the original signal and the low-pass,
band-pass, and high-pass outputs. Each row shows a periodogram.
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# firwin creates the filters, lfilter applies them to the signal.
from scipy.signal import firwin, lfilter

# Import the same sinusoid function used in Lab 1.
from signals import sinusoid


outputFolder = Path(__file__).with_name("output") / "filtering"
outputFolder.mkdir(parents=True, exist_ok=True)


# Use the number of samples and sampling rate given on slide 2.
nSamples = 2048
samplingFrequency = 1024
samplingInterval = 1 / samplingFrequency
timeSamples = np.arange(nSamples) * samplingInterval

# Generate the 3 sinusoids with the given  amplitudes and phases.
signal1 = sinusoid(timeSamples, amp=10.0, f0=100.0, phi0=0.0)
signal2 = sinusoid(timeSamples, amp=5.0, f0=200.0, phi0=np.pi / 6)
signal3 = sinusoid(timeSamples, amp=2.5, f0=300.0, phi0=np.pi / 4)
inputSignal = signal1 + signal2 + signal3

# Design the filters.
# Because this is python I am using `firwin`:
#   https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.firwin.html
#
# LowPassFilterDemo.m. uses order 30
filterOrder = 30

# firwin asks for numtaps (number of coefficients), which is order + 1.
numTaps = filterOrder + 1
lowPass = firwin(numtaps=numTaps, cutoff=150, pass_zero="lowpass", window="hamming", fs=samplingFrequency)
bandPass = firwin(numtaps=numTaps, cutoff=[150, 250], pass_zero="bandpass", window="hamming", fs=samplingFrequency)
highPass = firwin(numtaps=numTaps, cutoff=250, pass_zero="highpass", window="hamming", fs=samplingFrequency)

# Filter the original input signal 3 separate times, once with each filter.
# [1.0] tells lfilter to use input samples ONLY.
# The results below keep 100 Hz, 200 Hz, and 300 Hz, respectively.
output1 = lfilter(lowPass, [1.0], inputSignal)
output2 = lfilter(bandPass, [1.0], inputSignal)
output3 = lfilter(highPass, [1.0], inputSignal)

# Plot the input and output periodograms.
frequencies = np.fft.rfftfreq(nSamples, d=samplingInterval)
signalList = [
    ("Input: 100 + 200 + 300 Hz", inputSignal),
    ("Filter 1: low-pass, keeps 100 Hz", output1),
    ("Filter 2: band-pass, keeps 200 Hz", output2),
    ("Filter 3: high-pass, keeps 300 Hz", output3),
]

fig, axes = plt.subplots(4, 1, figsize=(9, 10))
for axis, (title, signalValues) in zip(axes, signalList):
    fftMagnitude = np.abs(np.fft.rfft(signalValues))
    axis.plot(frequencies, fftMagnitude)
    axis.set_title(title)
    axis.set_xlabel("Frequency (Hz)")
    axis.set_ylabel("|FFT|")
    axis.grid(alpha=0.25)

# Save one figure containing all periodograms.
fig.tight_layout()
fig.savefig(outputFolder / "filtering.png", dpi=150)
plt.close(fig)

print(f"Nyquist frequency limit: {samplingFrequency / 2:g} Hz")
print(f"Saved plots to: {outputFolder}")
