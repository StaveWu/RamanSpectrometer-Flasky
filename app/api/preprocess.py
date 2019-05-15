from . import api
from ..preprocessing import debackground, conventional, denoise
from ..models import Spectrum
from flask import jsonify, request
from .utils import get_property


@api.route('/denoises/dae', methods=['POST'])
def dae():
    spectrum = Spectrum.from_json(request.json)
    denoisy_spec = denoise.dae(spectrum)
    return jsonify(denoisy_spec.to_json())


@api.route('/denoises/sgfilter', methods=['POST'])
def sgfilter():
    spectrum = Spectrum.from_json(request.json)
    order = int(get_property(request.json, 'order'))
    window_length = int(get_property(request.json, 'windowLength'))
    denoisy_spec = denoise.sgfilter(spectrum, order, window_length)
    return jsonify(denoisy_spec.to_json())


@api.route('/denoises/wden', methods=['POST'])
def wden():
    spectrum = Spectrum.from_json(request.json)
    denoisy_spec = denoise.wavelet(spectrum)
    return jsonify(denoisy_spec.to_json())


@api.route('/conventionals/scale', methods=['POST'])
def scale():
    spectrum = Spectrum.from_json(request.json)
    scaled_spec = conventional.scale(spectrum)
    return jsonify(scaled_spec.to_json())


@api.route('/conventionals/minmax-scale', methods=['POST'])
def minmax_scale():
    spectrum = Spectrum.from_json(request.json)
    minmax_spec = conventional.minmax_scale(spectrum)
    return jsonify(minmax_spec.to_json())


@api.route('/debackgrounds/airpls', methods=['POST'])
def airPLS():
    spectrum = Spectrum.from_json(request.json)
    lambda_ = int(get_property(request.json, 'lambda'))
    dbg_spec = debackground.airPLS(spectrum, lambda_)
    return jsonify(dbg_spec.to_json())



