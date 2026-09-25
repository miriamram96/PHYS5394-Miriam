# Lab 1

**Author:** Miriam Ramos Arevalo  
**Date:** September 2026

This lab has two parts:

1. **Part 1:** create 8 discrete time signals and plot each signal against time.
2. **Part 2:** use the FFT to see which frequencies are present in each signal.

The code saves one image per signal in the `output` folder. 
Each image shows the time domain signal first and its periodogram below. 

_Note:_ The [sinusoid image](output/sinusoid.png) also includes the extra
frequency change comparison discussed in [Slide 14](<Lab Topic 1_1.pdf#page=14>).


## Files in this directory:

- `signals.py`: stores the functions that create the 8 signals. It does not run
  by itself.
- `run.py`: imports the functions from `signals.py`, creates all signals,
  computes their FFTs, makes the plots, and saves the results. This is the file
  you run.
- `output/`: contains the output images.
- `Lab Topic 1_1.pdf`: the lab instructions provided in Teams.


## How to run the lab?

From this directory, run:

```bash
python3 run.py
```

The code requires `NumPy` and `Matplotlib`.


## Signals created for this Lab

The script creates the 8 signals listed in the assignment:

1. Quadratic chirp
2. Sinusoid
3. Linear chirp
4. Sine-Gaussian
5. Frequency Modulated (FM) sinusoid
6. Amplitude Modulated (AM) sinusoid
7. AM-FM sinusoid
8. Linear transient chirp


## Sampling interval calculation

We use the same values provided in
`DATASCIENCE_COURSE/SIGNALS/testcrcbgenqcsig.m`: the quadratic chirp
coefficients `a1 = 10`, `a2 = 3`, and `a3 = 3`, the amplitude `A = 10`, and a
duration of one second. These values are used below to calculate the sampling
interval.

The MATLAB quadratic chirp example uses:

```text
signal(t) = A*sin(2*pi*phase(t))
phase(t) = a1*t + a2*t^2 + a3*t^3
frequency(t) = a1 + 2*a2*t + 3*a3*t^2
```

Using `a1 = 10`, `a2 = 3`, `a3 = 3`, and a duration of one second:

The code generates each signal from `t = 0` to `t = 1` second. During that
second, the quadratic chirp starts at 10 Hz and its frequency keeps increasing.
It reaches 25 Hz at `t = 1`, which is the highest frequency reached by any of
the signals in this lab. That is why 25 Hz is used to choose the sampling rate;
the rate needs to be high enough to sample the fastest signal correctly.

1. The maximum instantaneous frequency is
   `10 + 2(3)(1) + 3(3)(1)^2 = 25 Hz`.
2. Following the MATLAB example, `nyqFreq = 2(25) = 50 Hz`.
3. The sampling frequency is `5(50) = 250 Hz`.
4. The sampling interval is `1/250 = 0.004 seconds`.

Therefore, the code takes one sample every **0.004 seconds**.


### Sinusoid frequency comparison

[Slide 14](<Lab Topic 1_1.pdf#page=14>) asks us to change the sinusoid frequency in steps smaller than
`1/T`, where `T` is the duration of the signal in seconds.
Our signal lasts 1 second, so `1/T = 1 Hz`. The code compares 6.00, 6.50,
7.00, and 7.50 Hz. The changes are 0.50 Hz, which is smaller than 1 Hz.
The FFT frequency spacing is calculated using the formula from [Slide 13](<Lab Topic 1_1.pdf#page=13>):

```text
frequency spacing = 1 / (N * Delta)
                  = 1 / (251 * 0.004)
                  = 0.996 Hz
```

This means the FFT calculates frequency points approximately 0.996 Hz apart.
Our 0.50 Hz changes are smaller than that spacing, so the periodograms overlap,
but we can still see their magnitudes spread differently around 7 Hz.


## Interpreting the periodograms...

The Lab assignment defines a periodogram as the magnitude of the FFT. 
The x-axis shows frequency in Hz. In the y-axis,`|FFT|` shows how much of each frequency is in the signal. 

- **[Quadratic chirp](output/quadratic_chirp.png) and
  [linear chirp](output/linear_chirp.png):** Their frequencies change as time
  passes. Therefore, their periodograms contain a range of frequencies instead
  of a single sharp peak.
- **[Sinusoid](output/sinusoid.png):** The code sets the sinusoid frequency to
  7 Hz using `f0=7.0`.
  Therefore, the periodogram has its tallest peak near 7 Hz, showing that 7 Hz
  is the strongest frequency in the signal.
- **[Sine-Gaussian](output/sine_gaussian.png):** The code sets the sinusoid
  frequency to 15 Hz. A Gaussian envelope makes the signal last for only a
  short time, causing its FFT magnitude to spread across frequencies near 15
  Hz instead of producing one sharp peak.
- **[FM sinusoid](output/fm_sinusoid.png):** The code sets the central frequency
  to 10 Hz and changes it back and forth at a rate of 2 Hz. This frequency
  modulation produces multiple peaks around 10 Hz in the periodogram, rather
  than one sharp peak.
- **[AM sinusoid](output/am_sinusoid.png):** The code starts with a 15 Hz
  sinusoid and changes its amplitude at a rate of 2 Hz. This amplitude
  modulation produces peaks at `15 - 2 = 13 Hz` and `15 + 2 = 17 Hz` in the
  periodogram.
- **[AM-FM sinusoid](output/am_fm_sinusoid.png):** both its amplitude and
  frequency change, so it produces more peaks than the AM or FM signal alone.
- **[Linear transient chirp](output/linear_transient_chirp.png):** The signal is
  active only from 0.25 to 0.75 seconds, and its frequency increases during
  that interval. Its periodogram has its strongest peak near 6 Hz, with energy
  spread across nearby frequencies because the frequency changes over time and
  the signal lasts only 0.50 seconds.


## Variable names

These are some of the main variables used repeatedly in the Python scripts. The units are shown in parentheses.

- `timeSamples`: times at which the signal is calculated (sec).
- `signalValues`: calculated signal value at each time.
- `amp`: amplitude/height of the signal.
- `phi0`: phase at the beginning of the signal (rad).


## MATLAB references

- `DATASCIENCE_COURSE/SIGNALS/signals.mlx`
- `DATASCIENCE_COURSE/SIGNALS/testcrcbgenqcsig.m`
- `DATASCIENCE_COURSE/SIGNALS/crcbgenqcsig.m`
