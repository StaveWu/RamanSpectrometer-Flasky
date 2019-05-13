from flask import jsonify, request
from . import api
from ..repositories import SpectraRepository
from ..models import Spectra


@api.route('/spectras')
def load_spectras():
    count = request.args.get('count', 8, type=int)
    spectras = SpectraRepository.find_spectra_order_by_timestamp(count)
    return jsonify({
        'spectras': [spec.to_json() for spec in spectras]
    })


@api.route('/spectras/<int:id>')
def get_spectra(id):
    spectra = SpectraRepository.find_spectra_by_id(id)
    return jsonify(spectra.to_json())


@api.route('/spectras', methods=['POST'])
def add_spectra():
    spectra = Spectra.from_json(request.json)
    SpectraRepository.save_spectra(spectra)
    return jsonify(spectra.to_json())

