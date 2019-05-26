from . import api
from flask import request, jsonify
from ..detecting.models import Component, ComponentModel
from ..detecting.repositories import ComponentRepository, ComponentModelRepository, SpectraRepository


@api.route('/components')
def load_components():
    comps = ComponentRepository.find_all()
    return jsonify({
        'components': [comp.to_json() for comp in comps]
    })


@api.route('/components', methods=['POST'])
def add_component():
    comp = Component.from_json(request.json)
    ComponentRepository.save_component(comp)

    model = ComponentModel.create_model(comp.id, ComponentRepository.find_all())
    model.fit(SpectraRepository.find_all())
    ComponentModelRepository.save_model(model)
    return jsonify(comp.to_json())


@api.route('/components/<int:id>', methods=['DELETE'])
def remove_component(id):
    comp = ComponentRepository.delete_by_id(id)
    ComponentModelRepository.delete_by_id(id)
    return jsonify(comp.to_json())


@api.route('/components/<int:id>', methods=['PATCH'])
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

