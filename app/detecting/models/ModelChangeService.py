"""
确保模型状态数据库和模型文件存储的最终一致性
"""

from ..repositories import ModelStateRepository, ComponentModelRepository
from threading import Thread
from flask import current_app
from .detecting import ComponentModel, ModelState, State


def delete_by_id(comp_id):
    ModelStateRepository.delete_by_id(comp_id)
    ComponentModelRepository.delete_by_id(comp_id)


def async_fit_model(comp_id, spectra):
    model = ComponentModelRepository.find_by_id(comp_id)
    state = ModelStateRepository.find_by_id(comp_id)
    state.state = State.BUSY
    ModelStateRepository.update_state(state)

    def retrain_model_task(app, model, spectra):
        model.fit(spectra)
        state.state = State.ONLINE
        with app.app_context():
            ComponentModelRepository.save_model(model)
            ModelStateRepository.update_state(state)

    thread = Thread(target=retrain_model_task,
                    args=(current_app._get_current_object(), model, spectra))
    thread.setDaemon(True)
    thread.start()


def async_create_model(comp_id, comps, spectra):
    ComponentModelRepository.delete_by_id(comp_id)
    ModelStateRepository.delete_by_id(comp_id)

    state = ModelState(comp_id, State.BUSY)
    ModelStateRepository.save_state(state)

    def create_model_task(app, id, comps, spectra):
        model = ComponentModel.create_model(id, comps)
        model.fit(spectra)
        state.state = State.ONLINE
        with app.app_context():
            ComponentModelRepository.save_model(model)
            ModelStateRepository.update_state(state)

    # start a thread to handle this expensive work
    thread = Thread(target=create_model_task,
                    args=(current_app._get_current_object(), comp_id, comps, spectra))
    thread.start()





