"""
Functions for generating the discrete time signals for Lab 1.

    This file only stores the signal functions. 
    Run `python run.py` to generate the signals and plots.
    
Author: Miriam Ramos Arevalo
Date: September 2026
"""

from traitlets import This

import numpy as np


def quadratic_chirp(timeSamples, amp, qcCoefs):
    """Generate a quadratic chirp signal.

    Parameters:
        timeSamples: Times at which the signal is calculated (sec).
        amp: Signal amplitude.
        qcCoefs: Quadratic chirp coefficients [a1, a2, a3].
    Returns:
        signalValues: Generated signal values.
    """
    a1, a2, a3 = qcCoefs
    # instPhase is the instantaneous phase at each sample time.
    instPhase = a1 * timeSamples + a2 * timeSamples**2 + a3 * timeSamples**3
    signalValues = amp * np.sin(2 * np.pi * instPhase)
    return signalValues


def sinusoid(timeSamples, amp, f0, phi0):
    """Generate a sinusoid.

    Parameters:
        f0: Frequency of the sinusoid (Hz).
        phi0: Starting phase (rad).
    Returns:
        signalValues: Generated signal values.
    """
    signalValues = amp * np.sin(2 * np.pi * f0 * timeSamples + phi0)
    return signalValues


def linear_chirp(timeSamples, amp, f0, f1, phi0):
    """Generate a linear chirp.

    Parameters:
        f0: Initial frequency of the chirp (Hz).
        f1: Frequency change rate of the chirp (Hz/sec).
    Returns:
        signalValues: Generated signal values.
    """
    # instPhase is the instantaneous phase at each sample time.
    instPhase = f0 * timeSamples + 0.5 * f1 * timeSamples**2
    signalValues = amp * np.sin(2 * np.pi * instPhase + phi0)
    return signalValues


def sine_gaussian(timeSamples, amp, t0, sigma, f0, phi0):
    """Generate a sinusoid inside a Gaussian envelope.

    Parameters:
        t0: Center or delay of the pulse, where Gaussian peak occurs (sec).
        sigma: Standard deviation of the Gaussian distribution, 
            which controls the width (duration) of the envelope.(sec).
        f0: frequency of the sinusoid inside the envelope or
            carrier frequency (Hz).
    Returns:
        signalValues: Generated signal values.
    """
    envelope = np.exp(-((timeSamples - t0) ** 2) / (2 * sigma**2))
    signalValues = amp * envelope * np.sin( 2 * np.pi * f0 * timeSamples + phi0)
    return signalValues


def fm_sinusoid(timeSamples, amp, b, f0, f1):
    """Generate a Frequency Modulated (FM) sinusoid.

    Parameters:
        b: Amount of frequency modulation, represents the peak phase deviation (rad).
        f0: Carrier frequency (Hz).
        f1: Modulating frequency (Hz).
    Returns:
        signalValues: Generated signal values.
    """
    # instPhase is the instantaneous phase at each sample time (rad).
    instPhase = 2 * np.pi * f0 * timeSamples + b * np.cos(2 * np.pi * f1 * timeSamples)
    signalValues = amp * np.sin(instPhase)
    return signalValues


def am_sinusoid(timeSamples, amp, f0, f1, phi0):
    """Generate an Amplitude Modulated (AM) sinusoid.

    Parameters:
        f0: Frequency of the sinusoid whose amplitude is changed (Hz).
        f1: Frequency of the amplitude modulation (Hz).
    Returns:
        signalValues: Generated signal values.
    """
    envelope = np.cos(2 * np.pi * f1 * timeSamples)
    signalValues = amp * envelope * np.sin(2 * np.pi * f0 * timeSamples + phi0)
    return signalValues


def am_fm_sinusoid(timeSamples, amp, b, f0, f1):
    """Generate an Amplitude and Frequency-Modulated (AM-FM) sinusoid.

    Parameters:
        f0: Carrier frequency of the sinusoid (Hz).
        f1: Modulating frequency (Hz).
    Returns:
        signalValues: Generated signal values.
    """
    envelope = np.cos(2 * np.pi * f1 * timeSamples)
    # instPhase is the instantaneous phase at each sample time (rad).
    instPhase = 2 * np.pi * f0 * timeSamples + b * np.cos(2 * np.pi * f1 * timeSamples)
    signalValues = amp * envelope * np.sin(instPhase)
    return signalValues


def linear_transient_chirp(timeSamples, amp, ta, f0, f1, phi0, length):
    """Generate a linear chirp that is active for a limited time.

    Parameters:
        ta: Starting time of the chirp (sec).
        f0: Starting frequency of the chirp (Hz).
        f1: Controls the frequency increase (Hz/sec). 
        length: Duration of the chirp (sec).
    Returns:
        signalValues: Generated signal values.
    """
    
    # This creates an array of zeros with the same length as timeSamples. 
    # The entire signal initially has a value of zero.
    signalValues = np.zeros_like(timeSamples, dtype=float)

    # The chirp is only active from ta to ta + length.
    withinChirp = (timeSamples >= ta) & (timeSamples <= ta + length)

    # The formula uses (t - ta) while the chirp is active...
    shiftedTime = timeSamples[withinChirp] - ta

    # instPhase is the instantaneous phase while the chirp is active.
    # Its frequency starts at f0 and increases by 2*f1 Hz each second.
    instPhase = f0 * shiftedTime + f1 * shiftedTime**2

    # Fill in the chirp values, the rest of the signal stays at zero.
    signalValues[withinChirp] = amp * np.sin(2 * np.pi * instPhase + phi0)
    return signalValues

