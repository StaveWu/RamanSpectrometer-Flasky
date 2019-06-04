from flask import jsonify, request
from . import api
from ..detecting.repositories import SpectraRepository, ComponentModelRepository
from ..detecting.models import Spectrum, DetectResult


@api.route('/spectra')
def load_spectra():
    count = request.args.get('count', 8, type=int)
    spectra = SpectraRepository.find_by_timestamp_desc(count)
    return jsonify({
        'spectra': [spec.to_json() for spec in spectra]
    })


@api.route('/spectra/<int:id>')
def get_spectrum(id):
    spectrum = SpectraRepository.find_by_id(id)
    return jsonify(spectrum.to_json())


@api.route('/spectra', methods=['POST'])
def add_spectrum():
    spectrum = Spectrum.from_json(request.json)
    SpectraRepository.save_spectrum(spectrum)
    return jsonify(spectrum.to_json())


@api.route('/spectra/<int:id>', methods=['PATCH'])
def tag_spectrum(id):
    detect_result = DetectResult.from_json(request.json)

    spectrum = SpectraRepository.find_by_id(id)
    spectrum.set_component(detect_result)
    SpectraRepository.save_spectrum(spectrum)

    return jsonify({})


@api.route('/spectra/<int:id>/components', methods=['POST'])
def detect_components(id):
    spec = Spectrum.from_json(request.json)
    model = ComponentModelRepository.find_by_id(id)
    detect_results = model.predict(spec)
    return jsonify({
        'results': [res.to_json() for res in detect_results]
    })

