from ...algorithms.detect import ModelFactory, generate_train_data
from .spectra import Component
from typing import List


class StateWatcher:
    def online(self):
        pass

    def offline(self):
        pass

    def busy(self):
        pass


class ComponentModel:
    """Entity"""
    def __init__(self, comp_id, model):
        self._comp_id = comp_id
        self.delegate = model
        self.state_watchers: List[StateWatcher] = []

    @property
    def comp_id(self):
        return self._comp_id

    def register_state_watcher(self, watcher):
        self.state_watchers.append(watcher)

    def unregister_state_watcher(self, watcher):
        self.state_watchers.remove(watcher)

    def predict(self, spectra):
        pass

    def fit(self, spectra):
        pass

    @staticmethod
    def create_model(id, comps: List[Component]):
        xs, ys = generate_train_data([c.data_frame() for c in comps])
        model = ModelFactory.new_initial_transferred_model(xs, ys)
        return ComponentModel(id, model)



