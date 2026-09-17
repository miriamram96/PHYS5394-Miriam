"""
Functions for generating the discrete time signals in Lab 1.

Note: 
    Parameters are explained when they first appear and are not repeated in later
    functions.

Author: Miriam Ramos Arevalo
Date: September 2026
"""

import numpy as np


def quadratic_chirp(timeSamples, amp, qcCoefs):
    """Generate a quadratic chirp signal.

    Parameters:
        timeSamples: Times at which the signal is calculated (sec).
        amp: Signal amplitude.
        qcCoefs: Quadratic chirp coefficients [a1, a2, a3].
    Returns:
        sigVec: Generated signal values.
    """
    a1, a2, a3 = qcCoefs
    phaseVec = a1 * timeSamples + a2 * timeSamples**2 + a3 * timeSamples**3
    sigVec = amp * np.sin(2 * np.pi * phaseVec)
    return sigVec


def sinusoid(timeSamples, amp, f0, phi0):
    """Generate a sinusoid.

    Parameters:
        f0: Starting frequency (Hz).
        phi0: Starting phase (rad).
    Returns:
        sigVec: Generated signal values.
    """
    sigVec = amp * np.sin(2 * np.pi * f0 * timeSamples + phi0)
    return sigVec


def linear_chirp(timeSamples, amp, f0, f1, phi0):
    """Generate a linear chirp.

    Parameters:
        f1: Frequency change parameter for chirps (Hz/sec) or modulation
            frequency for AM/FM signals (Hz).
    Returns:
        sigVec: Generated signal values.
    """
    phaseVec = f0 * timeSamples + 0.5 * f1 * timeSamples**2
    sigVec = amp * np.sin(2 * np.pi * phaseVec + phi0)
    return sigVec


def sine_gaussian(timeSamples, amp, t0, sigma, f0, phi0):
    """Generate a sinusoid inside a Gaussian envelope.

    Parameters:
        t0: Center time of the envelope (sec).
        sigma: Width of the envelope (sec).
    Returns:
        sigVec: Generated signal values.
    """
    envelope = np.exp(-((timeSamples - t0) ** 2) / (2 * sigma**2))
    sigVec = amp * envelope * np.sin(2 * np.pi * f0 * timeSamples + phi0)
    return sigVec


def fm_sinusoid(timeSamples, amp, b, f0, f1):
    """Generate a frequency-modulated sinusoid.

    Parameters:
        b: Amount of frequency modulation (rad).
    Returns:
        sigVec: Generated signal values.
    """
    phaseVec = 2 * np.pi * f0 * timeSamples + b * np.cos(
        2 * np.pi * f1 * timeSamples)
    sigVec = amp * np.sin(phaseVec)
    return sigVec


def am_sinusoid(timeSamples, amp, f0, f1, phi0):
    """Generate an amplitude-modulated sinusoid.

    Returns:
        sigVec: Generated signal values.
    """
    envelope = np.cos(2 * np.pi * f1 * timeSamples)
    sigVec = amp * envelope * np.sin(2 * np.pi * f0 * timeSamples + phi0)
    return sigVec


def am_fm_sinusoid(timeSamples, amp, b, f0, f1):
    """Generate an amplitude- and frequency-modulated sinusoid.

    Returns:
        sigVec: Generated signal values.
    """
    envelope = np.cos(2 * np.pi * f1 * timeSamples)
    phaseVec = 2 * np.pi * f0 * timeSamples + b * np.cos(
        2 * np.pi * f1 * timeSamples)
    sigVec = amp * envelope * np.sin(phaseVec)
    return sigVec


def linear_transient_chirp(timeSamples, amp, ta, f0, f1, phi0, length):
    """Generate a linear chirp that is active for a limited time.

    Parameters:
        ta: Starting time of the chirp (sec).
        length: Duration of the chirp (sec).
    Returns:
        sigVec: Generated signal values.
    """
    sigVec = np.zeros_like(timeSamples, dtype=float)
    activeSamples = (timeSamples >= ta) & (timeSamples <= ta + length)
    shiftedTime = timeSamples[activeSamples] - ta

    phaseVec = f0 * shiftedTime + f1 * shiftedTime**2
    sigVec[activeSamples] = amp * np.sin(2 * np.pi * phaseVec + phi0)
    return sigVec
