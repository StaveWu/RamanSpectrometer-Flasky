"""
algorithms facade
"""

from .spectra import Spectrum
from app.algorithms import debackground, denoise, conventional
import numpy as np


def airPLS(spec: Spectrum, lambda_):
    data = np.array([spec.raman_shift, debackground.airPLS(spec.intensity, lambda_=lambda_)]).T
    name = '{}-airPLS'.format(spec.name)
    return Spectrum(name, data)


def minmax_scale(spec: Spectrum):
    data = np.array([spec.raman_shift, conventional.minmax_scale(spec.intensity)]).T
    name = '{}-minmax-scale'.format(spec.name)
    return Spectrum(name, data)


def scale(spec: Spectrum):
    data = np.array([spec.raman_shift, conventional.scale(spec.intensity)]).T
    name = '{}-scale'.format(spec.name)
    return Spectrum(name, data)


def sgfilter(spec: Spectrum, order: int, window_length: int):
    data = np.array([spec.raman_shift, denoise.savgol_filter(spec.intensity, window_length, order)]).T
    name = '{}-sgfilter'.format(spec.name)
    return Spectrum(name, data)


def wden(spec: Spectrum):
    data = np.array([spec.raman_shift, denoise.wavelet(spec.intensity)]).T
    name = '{}-wden'.format(spec.name)
    return Spectrum(name, data)


def dae(spec: Spectrum):
    data = np.array([spec.raman_shift, denoise.dae(spec.intensity)]).T
    name = '{}-dae'.format(spec.name)
    return Spectrum(name, data)



