from ...algorithms.detect import ModelFactory
from ...algorithms.data_generation import generate_train_data, to_int_index
from .spectra import Component, Spectrum
from typing import List
import pandas as pd
import numpy as np
from enum import Enum


class ModelState(Enum):
    ONLINE = 'online',
    OFFLINE = 'offline',
    BUSY = 'busy'


class ComponentModel:
    """Entity"""
    def __init__(self, comp_id, model, state='online'):
        self._comp_id = comp_id
        self.delegate = model
        self._state = ModelState(state)

    @property
    def comp_id(self):
        return self._comp_id

    @property
    def state(self):
        return self._state.value

    def predict(self, spectra):
        pass

    def fit(self, spectra: List[Spectrum]):
        self._state = ModelState.BUSY
        # alignment first since some spectrum's raman shift is not the same
        df = pd.concat([spec.series() for spec in spectra], axis=1)
        df.fillna(method='ffill')
        df.fillna(method='bfill')
        # change to int raman shift
        df = to_int_index(df)
        # get xs and ys for training
        xs = df.values.T
        ys = np.array([self.comp_id in spec.component_ids for spec in spectra]).astype('int')
        self.delegate.fit(xs, ys)
        self._state = ModelState.ONLINE

    @staticmethod
    def create_model(id, comps: List[Component]):
        xs, ys = generate_train_data([c.data_frame() for c in comps])
        model = ModelFactory.new_initial_transferred_model(xs, ys)
        return ComponentModel(id, model)

    def to_json(self):
        return {
            'id': self.comp_id,
            'state': self.state
        }



