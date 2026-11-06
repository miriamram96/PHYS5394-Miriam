# Miriam Ramos Arevalo
# November 2026
# Lab Topic 2_2 - Slide 7

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch, firwin2, fftconvolve, spectrogram

# Read the time and data columns from the provided file (testData.txt).
data_file = Path(__file__).resolve().parent / "testData.txt"
time, data = np.loadtxt(data_file, unpack=True)
sampling_frequency = 1 / (time[1] - time[0])

# The signal starts after 5 sec. 
# Estimate the noise PSD using only the earlier data, 
# so the signal is not included in the noise estimate.
noise = data[time < 5.0]
frequencies, noise_psd = welch(
    noise, fs=sampling_frequency, nperseg=1024
)

# statgaussnoisegen.m designs an FIR filter using the square root of a PSD.
# For whitening, use the inverse square root instead. This reduces the
# frequencies with more noise and makes the noise PSD approx. flat.
filter_order = 500
whitening_gain = 1 / np.sqrt(noise_psd)
whitening_filter = firwin2(
    filter_order + 1, frequencies, whitening_gain, fs=sampling_frequency)

# Apply the whitening filter to the full data.
# mode="same" keeps the centered output the same length as data, so it
# matches the time array. 
whitened_data = fftconvolve(data, whitening_filter, mode="same")

# Compare the time series before and after whitening.
fig, axes = plt.subplots(2, 1, sharex=True, figsize=(10, 6))
for ax, values, title in zip(
    axes, [data, whitened_data], ["Before whitening", "After whitening"]):
    ax.plot(time, values, linewidth=0.6)
    ax.set_title(title)
    ax.set_ylabel("Data")
axes[-1].set_xlabel("Time (sec)")
fig.tight_layout()

# Save the timeseries plot.
fig.savefig(data_file.parent / "time_series.png", dpi=150)

# A spectrogram shows how the frequency content changes over time.
# Use the same window length and overlap for both spectrograms.
fig, axes = plt.subplots(2, 1, sharex=True, sharey=True, figsize=(10, 7))
for ax, values, title in zip(
    axes, [data, whitened_data], ["Before whitening", "After whitening"]):
    freq, segment_time, power = spectrogram(
        values, fs=sampling_frequency, nperseg=512, noverlap=384)
    
    # Show power on a log scale.
    power_db = 10 * np.log10(np.maximum(power, np.finfo(float).tiny))
    
    # Keep the color in the plot looking good!
    color_min, color_max = np.percentile(power_db, [5, 99])
    image = ax.pcolormesh(
        segment_time + time[0], freq, power_db, shading="auto",
        vmin=color_min, vmax=color_max)
    
    ax.set_title(title)
    ax.set_ylabel("Frequency (Hz)")
    fig.colorbar(image, ax=ax, label="PSD (dB)")
axes[-1].set_xlabel("Time (s)")
fig.tight_layout()

# Save the spectrogram plot.
fig.savefig(data_file.parent / "spectrograms.png", dpi=150)

plt.show()
