from . import api
from ..repositories import ComponentRepository
from flask import request, jsonify
from ..models import Component


@api.route('/components')
def load_components():
    comps = ComponentRepository.find_all()
    return jsonify({
        'components': [comp.to_json() for comp in comps]
    })


@api.route('/components', method=['POST'])
def add_component():
    comp = Component.from_json(request.json)
    ComponentRepository.save_component(comp)
    return jsonify(comp.to_json())


@api.route('/components/<int:id>', method=['DELETE'])
def remove_component(id):
    comp = ComponentRepository.delete_by_id(id)
    return jsonify(comp.to_json())


@api.route('/components/<int:id>', method=['PATCH'])
def update_component(id):
    d = request.json.copy()
    d['id'] = id
    comp = Component.from_json(d)
    ComponentRepository.save_component(comp)
    return jsonify(comp.to_json())


@api.route('/components')
def get_component():
    id = request.args.get('id', type=int)
    comp = ComponentRepository.find_by_id(id)
    return jsonify(comp.to_json())

