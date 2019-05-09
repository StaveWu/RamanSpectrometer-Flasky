from flask import jsonify, request
from . import api
from ..models import Spectra


@api.route('/spectras')
def load_spectras():
    count = request.args.get('count', 8, type=int)
    spectras = Spectra.query.order_by(Spectra.timestamp.desc()).count(count)
    return jsonify({
        spectras: 'hello'
    })


@api.route('/spectras/<int:id>')
def get_spectra(id):
    spectra = Spectra.query.get_or_404(id)
    return jsonify(spectra.to_json())


@api.route('/spectras', methods=['POST'])
def add_spectra():
    pass

