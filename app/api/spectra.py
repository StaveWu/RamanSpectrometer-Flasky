from flask import jsonify, request
from . import api
from ..repositories import SpectraRepository, ComponentRepository
from ..models import Spectrum, TrainData
from ..exceptions import PropertyNotFoundError


@api.route('/spectra')
def load_spectra():
    count = request.args.get('count', 8, type=int)
    spectra = SpectraRepository.find_by_timestamp_desc(count)
    return jsonify({
        'spectra': [spec.to_json() for spec in spectra]
    })


@api.route('/spectra/<int:id>')
def get_spectrum(id):
    spectrum = SpectraRepository.find_by_id(id)  # may not found
    return jsonify(spectrum.to_json())


@api.route('/spectra', methods=['POST'])
def add_spectrum():
    spectrum = Spectrum.from_json(request.json)
    SpectraRepository.save_spectrum(spectrum)
    return jsonify(spectrum.to_json())


@api.route('/spectra/<int:id>', methods=['PATCH'])
def tag_spectrum(id):
    comp_id = request.json.get('compId')
    probability = request.json.get('probability')
    if not check_property(comp_id):
        raise PropertyNotFoundError('[compId] not found')
    if not check_property(probability):
        raise PropertyNotFoundError('[probability] not found')

    spectra = SpectraRepository.find_by_id(id)  # may not found
    spectra.set_component(comp_id, float(probability))
    SpectraRepository.save_spectrum(spectra)

    component = ComponentRepository.find_by_id(comp_id)
    spectras = SpectraRepository.find_all()
    component.retrain(TrainData(spectras))


def check_property(prop: str):
    return prop is not None and prop != ''

