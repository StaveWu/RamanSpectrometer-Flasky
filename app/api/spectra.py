from flask import jsonify, request
from . import api
from ..detecting.repositories import SpectraRepository, ComponentModelRepository
from ..detecting.models import Spectrum
from .utils import get_property


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
    comp_id = int(get_property(request.json, 'compId'))
    probability = float(get_property(request.json, 'probability'))

    # modify spectrum's label
    spectrum = SpectraRepository.find_by_id(id)  # may not found
    spectrum.set_component(comp_id, probability)
    SpectraRepository.save_spectrum(spectrum)

    # retrain component model
    model = ComponentModelRepository.find_by_id(comp_id)
    model.fit(SpectraRepository.find_all())
    ComponentModelRepository.save_model(model)

    return jsonify({})


