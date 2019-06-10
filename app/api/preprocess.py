from . import api
from ..preprocessing.models import Spectrum, PrerocessingService
from flask import jsonify, request
from ..utils import JsonWrapper


@api.route('/denoises/dae', methods=['POST'])
def dae():
    spectrum = Spectrum.from_json(request.json)
    denoisy_spec = PrerocessingService.dae(spectrum)
    return jsonify(denoisy_spec.to_json())


@api.route('/denoises/sgfilter', methods=['POST'])
def sgfilter():
    spectrum = Spectrum.from_json(request.json)
    params = JsonWrapper(request.json).get('params')
    order = params.get_strict('order', type=int)
    window_length = params.get_strict('windowLength', type=int)
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
    params = JsonWrapper(request.json).get('params')
    lambda_ = params.get_strict('lambda', type=int)
    dbg_spec = PrerocessingService.airPLS(spectrum, lambda_)
    return jsonify(dbg_spec.to_json())


@api.route('conventionals/cut-off', methods=['POST'])
def cut_off():
    spectrum = Spectrum.from_json(request.json)
    params = JsonWrapper(request.json).get('params')
    start = params.get_strict('start', type=int)
    end = params.get_strict('end', type=int)
    co_spec = PrerocessingService.cut_off(spectrum, start, end)
    return jsonify(co_spec.to_json())



