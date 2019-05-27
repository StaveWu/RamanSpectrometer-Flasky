from ...exceptions import IncompleteFieldError
from typing import List


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


class Spectrum(SpectrumBase):
    """Entity"""
    def __init__(self, id, name, data, timestamp=None, component_ids=None):
        super().__init__(name, data)
        self._id = id
        self._timestamp = timestamp
        self.label = Label(component_ids)

    @property
    def id(self):
        """read only"""
        return self._id

    @property
    def component_ids(self):
        return self.label.comp_ids

    @property
    def timestamp(self):
        return self._timestamp

    def set_component(self, comp_id, probability):
        self.label = self.label.to_label(comp_id, probability)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'data': self.data.tolist(),
            'timestamp': self.timestamp
        }

    @staticmethod
    def from_json(json_spectrum):
        id = json_spectrum.get('id')
        try:
            id = int(id)
        except TypeError:
            id = None
        name = json_spectrum.get('name')
        if name is None or name == '':
            raise IncompleteFieldError('json does not have a name')
        data = json_spectrum.get('data')
        if data is None or data == '':
            raise IncompleteFieldError('json does not have a data')
        return Spectrum(id, name, data)


class Component:
    """Entity"""
    def __init__(self, id, name, owned_spectra, formula=None):
        self._id = id
        self.name = name
        self.owned_spectra: List[SpectrumBase] = owned_spectra
        self.formula = formula

    @property
    def id(self):
        return self._id

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'formula': self.formula,
            'data': [spec.to_json() for spec in self.owned_spectra]
        }

    def data_frame(self):
        import pandas as pd
        df = pd.concat([pd.Series(name=self.name, index=cos.raman_shift, data=cos.intensity)
                          for cos in self.owned_spectra], axis=1)
        df = df.fillna(method='ffill')
        df = df.fillna(method='bfill')
        return df

    @staticmethod
    def from_json(json_spectrum):
        id = json_spectrum.get('id')
        try:
            id = int(id)
        except TypeError:
            id = None
        name = json_spectrum.get('name')
        if name is None or name == '':
            raise IncompleteFieldError('json does not have a name')
        data = json_spectrum.get('data')
        if data is None or data == '':
            raise IncompleteFieldError('json does not have a data')
        formula = json_spectrum.get('formula')
        return Component(id, name, data, formula)


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


class Label:
    """Value Object"""
    def __init__(self, comp_ids):
        self.comp_ids = comp_ids
        if not self.comp_ids:
            self.comp_ids = []

    def one_hot(self):
        pass

    def one_hot_int(self):
        pass

    def to_label(self, comp_id, probability):
        comp_ids = self.comp_ids.copy()
        if probability > 0.5:
            comp_ids.append(comp_id)
        else:
            comp_ids.remove(comp_id)
        return Label(comp_ids)

