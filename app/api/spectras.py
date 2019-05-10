from flask import jsonify, request
from . import api
from ..models import Spectra
from .. import db


@api.route('/spectras')
def load_spectras():
    count = request.args.get('count', 8, type=int)
    spectras = Spectra.query.order_by(Spectra.timestamp.desc()).limit(count)
    return jsonify({
        'spectras': [spec.to_json() for spec in spectras]
    })


@api.route('/spectras/<int:id>')
def get_spectra(id):
    spectra = Spectra.query.get_or_404(id)
    return jsonify(spectra.to_json())


@api.route('/spectras', methods=['POST'])
def add_spectra():
    print(request.json)
    spectra = Spectra.from_json(request.json)
    db.session.add(spectra)
    db.session.commit()
    return jsonify(spectra.to_json())

