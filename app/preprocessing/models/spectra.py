from ...exceptions import PropertyNotFoundError


class Spectrum:
    """Value object"""
    def __init__(self, name, data):
        self.name = name
        self._data = SpectrumData(data)

    @property
    def intensity(self):
        return self._data.intensity

    @property
    def raman_shift(self):
        return self._data.raman_shift

    @property
    def data(self):
        return self._data.data

    @staticmethod
    def from_json(json_spectrum):
        name = json_spectrum.get('name')
        if name is None or name == '':
            raise PropertyNotFoundError('json does not have a name')
        data = json_spectrum.get('data')
        if data is None or data == '':
            raise PropertyNotFoundError('json does not have a data')
        return Spectrum(name, data)

    def to_json(self):
        return {
            'name': self.name,
            'data': self.data,
        }


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


