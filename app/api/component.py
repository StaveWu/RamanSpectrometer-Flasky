from . import api
from flask import request, jsonify
from ..detecting.models import Component, ComponentModel
from ..detecting.repositories import ComponentRepository, ComponentModelRepository, SpectraRepository
from threading import Thread


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
    ComponentRepository.save_component(comp)
    return jsonify(comp.to_json())


@api.route('/components/<int:id>')
def get_component(id):
    comp = ComponentRepository.find_by_id(id)
    return jsonify(comp.to_json())


@api.route('/components/<int:id>/model', methods=['POST'])
def create_model(id):
    if not ComponentRepository.contains(id):
        raise ValueError('component corresponding to model is not exist')

    def create_model_task():
        ComponentModelRepository.delete_by_id(id)
        model = ComponentModel.create_model(id, ComponentRepository.find_all())
        model.fit(SpectraRepository.find_all())
        ComponentModelRepository.save_model(model)

    thread = Thread(target=create_model_task)
    thread.start()
    return jsonify({}), 202


@api.route('/components/<int:id>/model', methods=['PUT'])
def tune_model(id):
    model = ComponentModelRepository.find_by_id(id)
    model.fit(SpectraRepository.find_all())
    ComponentModelRepository.save_model(model)
    return jsonify({})


@api.route('/models')
def get_models():
    models = ComponentModelRepository.lightweight_find_all()
    return jsonify({
        'models': [model.to_json() for model in models]
    })
