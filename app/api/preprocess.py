from . import api
from ..models import Spectrum, PrerocessingService
from flask import jsonify, request
from .utils import get_property


@api.route('/denoises/dae', methods=['POST'])
def dae():
    spectrum = Spectrum.from_json(request.json)
    denoisy_spec = PrerocessingService.dae(spectrum)
    return jsonify(denoisy_spec.to_json())


@api.route('/denoises/sgfilter', methods=['POST'])
def sgfilter():
    spectrum = Spectrum.from_json(request.json)
    order = int(get_property(request.json, 'order'))
    window_length = int(get_property(request.json, 'windowLength'))
    denoisy_spec = PrerocessingService.sgfilter(spectrum, order, window_length)
    return jsonify(denoisy_spec.to_json())


@api.route('/denoises/wden', methods=['POST'])
def wden():
    spectrum = Spectrum.from_json(request.json)
    denoisy_spec = PrerocessingService.wden(spectrum)
    return jsonify(denoisy_spec.to_json())


@api.route('/conventionals/scale', methods=['POST'])
def scale():
    spectrum = Spectrum.from_json(request.json)
    scaled_spec = PrerocessingService.scale(spectrum)
    return jsonify(scaled_spec.to_json())


@api.route('/conventionals/minmax-scale', methods=['POST'])
def minmax_scale():
    spectrum = Spectrum.from_json(request.json)
    minmax_spec = PrerocessingService.minmax_scale(spectrum)
    return jsonify(minmax_spec.to_json())


@api.route('/debackgrounds/airpls', methods=['POST'])
def airPLS():
    spectrum = Spectrum.from_json(request.json)
    lambda_ = int(get_property(request.json, 'lambda'))
    dbg_spec = PrerocessingService.airPLS(spectrum, lambda_)
    return jsonify(dbg_spec.to_json())


