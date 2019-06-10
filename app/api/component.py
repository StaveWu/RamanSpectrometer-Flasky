from . import api
from flask import request, jsonify
from ..detecting.models import Component, ModelChangeService
from ..detecting.repositories import ComponentRepository, SpectraRepository, ModelStateRepository


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
    return jsonify(comp.to_json())


@api.route('/components/<int:id>', methods=['DELETE'])
def remove_component(id):
    ComponentRepository.delete_by_id(id)
    return jsonify({})


@api.route('/components/<int:id>', methods=['PATCH'])
def update_component(id):
    d = request.json.copy()
    d['id'] = id
    comp = Component.from_json(d)
    ComponentRepository.update_component(comp)
    return jsonify(comp.to_json())


@api.route('/components/<int:id>')
def get_component(id):
    comp = ComponentRepository.find_by_id(id)
    return jsonify(comp.to_json())


@api.route('/components/<int:id>/model', methods=['POST'])
def create_model(id):
    if not ComponentRepository.contains(id):
        raise ValueError('component corresponding to model is not exist')

    comps = ComponentRepository.find_all()
    spectra = SpectraRepository.find_all()
    ModelChangeService.async_create_model(id, comps, spectra)

    return jsonify({}), 202


@api.route('/components/<int:id>/model', methods=['PUT'])
def tune_model(id):
    spectra = SpectraRepository.find_all()
    ModelChangeService.async_fit_model(id, spectra)
    return jsonify({})


@api.route('/models')
def get_models():
    models = ModelStateRepository.find_all()
    return jsonify({
        'models': [model.to_json() for model in models]
    })


@api.route('/models/<int:id>')
def get_model(id):
    model = ModelStateRepository.find_by_id(id)
    return jsonify(model.to_json())


@api.route('/models/<int:id>', methods=['DELETE'])
def delete_model(id):
    ModelChangeService.delete_by_id(id)
    return jsonify({})
