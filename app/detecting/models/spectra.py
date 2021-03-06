from typing import List
from ..repositories.daos import SpectrumDAO, ComponentDAO
import pandas as pd
from ...utils import JsonWrapper


class DetectResult:
    """value object"""
    def __init__(self, comp_id, probability):
        self.comp_id = comp_id
        self.probability = probability

    def exist(self):
        return self.probability > 0.5

    def to_json(self):
        return {
            'id': self.comp_id,
            'probability': self.probability
        }

    @staticmethod
    def from_json(json_res):
        wrapper = JsonWrapper(json_res)
        comp_id = wrapper.get_strict('id', type=int)
        probability = wrapper.get_strict('probability', type=float)
        return DetectResult(comp_id, probability)


class SpectrumBase:
    """Entity"""

    def __init__(self, name, data):
        self.name = name
        self._data = SpectrumData(data)

    def truncate(self, start: int, end: int):
        self._data.truncate(start, end)

    @property
    def data(self):
        return self._data.data

    @data.setter
    def data(self, value):
        self._data = SpectrumData(value)

    @property
    def intensity(self):
        return self._data.intensity

    @property
    def raman_shift(self):
        return self._data.raman_shift

    def to_json(self):
        return {
            'name': self.name,
            'data': self.data.tolist(),
        }

    @staticmethod
    def from_json(json_spec):
        wrapper = JsonWrapper(json_spec)
        name = wrapper.get_strict('name')
        data = wrapper.get_strict('data')
        return SpectrumBase(name, data)


class Spectrum(SpectrumBase):
    """Entity"""

    def __init__(self, id, name, data, timestamp=None, component_ids=None):
        super().__init__(name, data)
        self.dao = SpectrumDAO(id=id, name=name, timestamp=timestamp)
        self.component_ids = component_ids if component_ids else []

    @property
    def id(self):
        """read only"""
        return self.dao.id

    @property
    def timestamp(self):
        return self.dao.timestamp

    def set_component(self, detect_result: DetectResult):
        if detect_result.exist():
            if detect_result.comp_id not in self.component_ids:
                self.component_ids.append(detect_result.comp_id)
        else:
            if detect_result.comp_id in self.component_ids:
                self.component_ids.remove(detect_result.comp_id)

    def is_existing(self, comp_id):
        return comp_id in self.component_ids

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'data': self.data.tolist(),
            'timestamp': self.timestamp
        }

    @staticmethod
    def from_json(json_spectrum):
        wrapper = JsonWrapper(json_spectrum)
        id = wrapper.get('id')
        name = wrapper.get_strict('name')
        data = wrapper.get_strict('data')
        return Spectrum(id, name, data)

    @staticmethod
    def of(dao: SpectrumDAO, data, comp_ids):
        return Spectrum(id=dao.id, name=dao.name, timestamp=dao.timestamp,
                        data=data, component_ids=comp_ids)

    def series(self):
        return pd.Series(index=self.raman_shift, data=self.intensity, name=self.id)


class Component:
    """Entity"""

    def __init__(self, id, name, owned_spectra, formula=None):
        self.dao = ComponentDAO(id=id, name=name, formula=formula)
        self.owned_spectra: List[SpectrumBase] = owned_spectra

    @property
    def id(self):
        return self.dao.id

    @property
    def name(self):
        return self.dao.name

    @name.setter
    def name(self, value):
        self.dao.name = value

    @property
    def formula(self):
        return self.dao.formula

    @formula.setter
    def formula(self, value):
        self.dao.formula = value

    def data_frame(self):
        df = pd.concat([pd.Series(name=self.id, index=cos.raman_shift, data=cos.intensity)
                        for cos in self.owned_spectra], axis=1)
        df = df.fillna(method='ffill')
        df = df.fillna(method='bfill')
        return df

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'formula': self.formula,
            'owned_spectra': [spec.to_json() for spec in self.owned_spectra]
        }

    @staticmethod
    def from_json(json_comp):
        wrapper = JsonWrapper(json_comp)
        id = wrapper.get('id')
        name = wrapper.get_strict('name')
        json_owned_spectra = wrapper.get_strict('owned_spectra')
        owned_spectra = [SpectrumBase.from_json(json_spec) for json_spec in json_owned_spectra]
        formula = wrapper.get('formula')
        return Component(id=id, name=name, owned_spectra=owned_spectra, formula=formula)

    @staticmethod
    def of(dao: ComponentDAO, owned_spectra):
        return Component(id=dao.id, name=dao.name,
                         owned_spectra=owned_spectra, formula=dao.formula)


class SpectrumData:
    """Value object"""

    def __init__(self, data):
        import numpy as np
        if not isinstance(data, (list, tuple, np.ndarray)):
            raise ValueError('spectra data expect list/tuple/np.ndarray but get {}'.format(type(data)))
        data_array = np.array(data)
        if data_array.ndim != 2 or data_array.shape[1] != 2:
            raise ValueError('spectra data shape is not correct: {}'.format(data_array.shape))
        self.data = np.array(data)

    def truncate(self, start, end):
        return SpectrumData(self.data[start:end])

    @property
    def intensity(self):
        return self.data[:, 1]

    @property
    def raman_shift(self):
        return self.data[:, 0]


