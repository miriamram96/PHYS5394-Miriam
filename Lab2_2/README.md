# Lab Topic 2_2

**Author:** Miriam Ramos Arevalo  
**Date:** November 2026

There is one folder for each task in `Lab Topic 2_2.pdf`. Where folder names are the slide numbers where the task is being described.

Slides 6 and 13 are written in MATLAB because they ask to use `colGaussNoiseDemo.m` and `statgaussnoisegen.m`. 

Slide 7 is in Python and needs NumPy, SciPy, and Matplotlib to run.

## Slide 6 - Colored Gaussian noise

*MATLAB. Modified from `NOISE/colGaussNoiseDemo.m`. Script`statgaussnoisegen.m` is copied from `NOISE/` and used without any changes.*

`colGaussNoiseDemo.m` is the original script provided but I have added labels and titles. It runs for 16384, 32768, and 65536 samples and plots the target and estimated PSDs, the time series, a zoomed view, and a histogram. 
To see the outputs in `MATLAB` run the script `colGaussNoiseDemo.m`, which is found in the `Slide6` folder.

**Why does the estimated PSD become smoother?**
The Welch window length stays at 256 samples, so with more samples there are more segments to average. Averaging more segments makes the estimate less noisy.

**Does the zoomed time series look like WGN (White Gaussian Noise)? How does it differ?**
We define White Gaussian Noise (WGN) as random noise whose values follow a Gaussian (normal) distribution and whose power is the same at all frequencies, so its PSD is flat and each sample is independent of the others.
Now, to anwer the question, it looks random, but it oscillates more regularly than white noise because its power is only between 100 and 300 Hz.

**Is the histogram still a Normal PDF?**
Yes, it is still bell shaped. Filtering Gaussian noise with a linear filter gives Gaussian noise.

## Slide 7 - Whitening the data

*Python. The filter design has been adapted from `NOISE/statgaussnoisegen.m`. `testData.txt` is copied from `NOISE/`.*

`whitenData.py` does the following:

1. Uses the data before 5 sec (only the noise with no signal) to estimate the noise PSD.
2. Designs a whitening filter the same way as `statgaussnoisegen.m`, but using 1/√PSD instead of √PSD, so the noise ends up with the same power at all frequencies (white).
3. Applies the filter to all the data and plots the time series and spectrograms before and after whitening.

To run this script go into `Slide7` folder and from the terminal or VS Code run:
```bash
python3 whitenData.py
```

**Is the presence of the signal clearer after whitening?**
Yes, in the spectrogram. After whitening, a chirp rising from about 20 to 50 Hz between about 7 sec and 9 sec can be seen. In the time series the signal is still not visible.

## Slide 13 - Simulated LIGO noise

*MATLAB. Adapted from `NOISE/colGaussNoiseDemo.m`. `statgaussnoisegen.m` and `iLIGOSensitivity.txt` are copied from `NOISE/` without changes.*

The script `simulateLIGONoise.m` does the following:

1. Squared the ASD values in `iLIGOSensitivity.txt` to get the target PSD.
2. Kept the PSD constant below 50 Hz and above 700 Hz, and added the endpoints needed for the filter.
3. Generated simulated LIGO noise using `statgaussnoisegen.m`, estimated its PSD with `pwelch`, and plotted the target on top for comparison.

The estimated PSD follows the overall shape of the target, with small fluctuations.

To run it, go to the `Slide13` folder in MATLAB and run `simulateLIGONoise.m`.
