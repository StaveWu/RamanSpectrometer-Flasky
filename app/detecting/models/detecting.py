from ...algorithms.detect import ModelFactory
from ...algorithms.data_generation import generate_train_data, to_int_index, zero_end_interpolation
from .spectra import Component, Spectrum, DetectResult
from typing import List, Union
import pandas as pd
import numpy as np
from enum import Enum
from ...utils import JsonWrapper


class State(Enum):
    ONLINE = 'online'
    OFFLINE = 'offline'
    BUSY = 'busy'


class ModelState:
    """Entity"""
    def __init__(self, comp_id, state=State.ONLINE):
        self._comp_id = comp_id
        self.state = state

    @property
    def comp_id(self):
        return self._comp_id

    def to_json(self):
        return {
            'id': self.comp_id,
            'state': self.state.value
        }

    @staticmethod
    def of(id, state_str):
        return ModelState(id, State(state_str))

    @staticmethod
    def from_json(json_res):
        wrapper = JsonWrapper(json_res)
        comp_id = wrapper.get_strict('compId', type=int)
        probability = wrapper.get_strict('probability', type=float)
        return DetectResult(comp_id, probability)


class ComponentModel:
    """Entity"""
    def __init__(self, comp_id, model):
        self._comp_id = comp_id
        self.delegate = model

    @property
    def comp_id(self):
        return self._comp_id

    def predict(self, target: Union[List[Spectrum], Spectrum]) -> List[DetectResult]:
        if not isinstance(target, (list, tuple)):
            target = [target]
        df = self._pre_process(target)
        xs = df.values.T
        ys = self.delegate.predict(xs).round()
        res = [DetectResult(self.comp_id, y) for y in ys]
        return res

    def fit(self, spectra: List[Spectrum]):
        df = self._pre_process(spectra)
        # get xs and ys for training
        xs = df.values.T
        ys = np.array([spec.is_existing(self.comp_id) for spec in spectra]).astype('int')
        self.delegate.fit(xs, ys, batch_size=4, epochs=20)

    @staticmethod
    def _pre_process(spectra):
        # alignment first since some spectrum's raman shift is not the same
        df = pd.concat([spec.series() for spec in spectra], axis=1)
        df.fillna(method='ffill')
        df.fillna(method='bfill')
        # change to int raman shift
        df = to_int_index(df)
        # interpolation from zero to end
        df = zero_end_interpolation(df)
        return df

    @staticmethod
    def create_model(id, comps: List[Component]):
        xs, ys = generate_train_data([c.data_frame() for c in comps])
        model = ModelFactory.new_initial_transferred_model(xs, ys)
        return ComponentModel(id, model)





