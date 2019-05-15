from ..repositories import SpectraRepository, ComponentRepository
from ..exceptions import PropertyNotFoundError


class SpectrumBase:
    """Entity"""
    def __init__(self, id, name, data):
        self._id = id
        self.name = name
        self._data = SpectrumData(data)

    @property
    def id(self):
        """read only"""
        return self._id

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


class Spectrum(SpectrumBase):
    """Entity"""
    def __init__(self, id, name, data, component_ids=None):
        super().__init__(id, name, data)
        self.label = Label(component_ids)
        # access id and timestamp by db generating
        spec_dao = SpectraRepository.SpectraDAO(name=self.name)
        if not self._id:
            self._id = spec_dao.id
        self._timestamp = spec_dao.timestamp

    @property
    def timestamp(self):
        return self._timestamp

    def set_component(self, comp_id, probability):
        self.label = self.label.to_label(comp_id, probability)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'data': self.data,
            'timestamp': self.timestamp
        }

    @staticmethod
    def from_json(json_spectrum):
        name = json_spectrum.get('name')
        if name is None or name == '':
            raise PropertyNotFoundError('json does not have a name')
        data = json_spectrum.get('data')
        if data is None or data == '':
            raise PropertyNotFoundError('json does not have a data')
        return Spectrum(None, name, data)


class StateWatcher:
    """interface"""
    def busy(self):
        pass

    def online(self):
        pass

    def offline(self):
        pass


class Component(StateWatcher):
    """Entity"""
    def __init__(self, id, name, comp_spectra, formula=None):
        super().__init__()
        self._id = id if id else self._generate_id()
        self.name = name
        self.comp_spectra = comp_spectra
        self.formula = formula
        self.state = None
        self.network = None

    def _generate_id(self):
        return ComponentRepository.ComponentDAO(name=self.name, formula=self.formula).id

    @property
    def id(self):
        return self._id

    def is_existing_on(self, spec: SpectrumBase):
        if not self.network:  # lazy load
            self.network = DetectionNetwork(self.id)
            self.network.register(self)
        pass

    def retrain(self, train_data):
        if not self.network:  # lazy load
            self.network = DetectionNetwork(self.id)
            self.network.register(self)
        self.network.fit(train_data.X, train_data.Y)

    def busy(self):
        self.state = 'busy'

    def online(self):
        self.state = 'online'

    def offline(self):
        self.state = 'offline'

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'formula': self.formula,
            'data': [spec.to_json() for spec in self.comp_spectra]
        }

    @staticmethod
    def from_json(json_spectrum):
        name = json_spectrum.get('name')
        if name is None or name == '':
            raise PropertyNotFoundError('json does not have a name')
        data = json_spectrum.get('data')
        if data is None or data == '':
            raise PropertyNotFoundError('json does not have a data')
        return Component(None, name, data)


class DetectionNetwork:
    """Entity"""
    def __init__(self, comp_id):
        self._comp_id = comp_id
        self.model = None
        self.state_watcher = None

    @property
    def comp_id(self):
        return self._comp_id

    def register(self, state_watcher: StateWatcher):
        self.state_watcher = state_watcher

    def predict(self, spec: SpectrumBase):
        pass

    def fit(self, xs, ys):
        self.state_watcher.busy()
        # fit data
        self.model.fit(xs, ys)
        self.state_watcher.online()


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


class TrainData:
    def __init__(self, spectra, bit_for_label=None):
        self.spectra = spectra
        if not self.spectra:
            self.spectra = []
        self.bit_for_label = bit_for_label

    @property
    def X(self):
        return self._alignment()

    @property
    def Y(self):
        res = [spec.label.one_hot_int() for spec in self.spectra]
        if self.bit_for_label:
            pass
        return res

    def _alignment(self):
        pass


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

