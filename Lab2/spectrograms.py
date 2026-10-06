"""
Part 3:
Make time frequency plots of the 8 signals.

The output of this script is on `output/spectrograms`, with one figure per signal.
Each figure shows a spectrogram: time on the horizontal axis,
frequency on the vertical axis, and color showing the magnitude.
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram
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


outputFolder = Path(__file__).with_name("output") / "spectrograms"
outputFolder.mkdir(parents=True, exist_ok=True)


# Use the given sampling frequency:
# Keep the Lab 1 interval from 0 --> 1 second.
samplingFrequency = 1024
samplingInterval = 1 / samplingFrequency
nSamples = samplingFrequency + 1
timeSamples = np.arange(nSamples) * samplingInterval

# Use the window length and overlap from the example:
windowLength = 256
window = np.hamming(windowLength)
overlap = 250

# Generate the same signals with the same parameters as Lab 1:
quadChirp = quadratic_chirp(timeSamples, amp=10.0, qcCoefs=[10.0, 3.0, 3.0])
sinusoidSignal = sinusoid(timeSamples, amp=1.0, f0=7.0, phi0=0.0)
linearChirp = linear_chirp(timeSamples, amp=1.0, f0=2.0, f1=8.0, phi0=0.0)
sineGaussian = sine_gaussian(timeSamples, amp=1.0, t0=0.50, sigma=0.10, f0=15.0, phi0=0.0)
fmSinusoid = fm_sinusoid(timeSamples, amp=1.0, b=2.0, f0=10.0, f1=2.0)
amSinusoid = am_sinusoid(timeSamples, amp=1.0, f0=15.0, f1=2.0, phi0=0.0)
amFmSinusoid = am_fm_sinusoid(timeSamples, amp=1.0, b=2.0, f0=15.0, f1=2.0)
transientChirp = linear_transient_chirp(timeSamples, amp=1.0, ta=0.25, f0=3.0, f1=6.0, phi0=0.0, length=0.50)

signalList = [
    ("quadratic_chirp", "Quadratic Chirp", quadChirp),
    ("sinusoid", "Sinusoid", sinusoidSignal),
    ("linear_chirp", "Linear Chirp", linearChirp),
    ("sine_gaussian", "Sine Gaussian", sineGaussian),
    ("fm_sinusoid", "Frequency Modulated (FM) Sinusoid", fmSinusoid),
    ("am_sinusoid", "Amplitude Modulated (AM) Sinusoid", amSinusoid),
    ("am_fm_sinusoid", "AM-FM Sinusoid", amFmSinusoid),
    ("linear_transient_chirp", "Linear Transient Chirp", transientChirp),
]


for fileName, title, signalValues in signalList:
    # SpecgrmQCDemo.m, uses:
    # [S,F,T] = spectrogram(sigVec,256,250,[],sampFreq);

    # In comparison, our Python call below uses:
    # signalValues for sigVec, and fs=samplingFrequency for sampFreq.
    # nperseg=256: goes over 256 samples at a time, using a Hamming window.
    # noverlap=250: reuse 250 samples, moving forward by 6 samples each time.
    # nfft=256: calculate a 256 point FFT for each part of the signal.
    # detrend=False: do not subtract the average from each piece.
    # mode="complex": return FFT results.
    # scaling="spectrum": use Python's spectrum scaling.
    # Python returns frequencies (F), times (T), and FFT results (S).
    # Where F labels the y-axis, T labels the x-axis,
    # and the magnitude of S determines the colors.
    frequencies, spectrogramTimes, fftValues = spectrogram(
        signalValues, fs=samplingFrequency, window=window,
        nperseg=windowLength, noverlap=overlap, nfft=windowLength,
        detrend=False, scaling="spectrum", mode="complex",
    )
    # Get the magnitude of the FFT results:
    fftMagnitude = np.abs(fftValues)

    # Plot spectrograms:
    fig, axis = plt.subplots(figsize=(9, 5))
    image = axis.pcolormesh(spectrogramTimes, frequencies, fftMagnitude, shading="auto", cmap="magma")
    axis.set_title(title)
    axis.set_xlabel("Time (sec)")
    axis.set_ylabel("Frequency (Hz)")
    # Adjust the vertical axis:
    axis.set_ylim(0, 40)
    fig.colorbar(image, ax=axis, label="Magnitude")
    fig.tight_layout()
    fig.savefig(outputFolder / f"{fileName}.png", dpi=150)
    plt.close(fig)

print(f"Saved plots to: {outputFolder}")
