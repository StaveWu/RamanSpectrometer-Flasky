from ..repositories import SpectraRepository, ComponentRepository
from ..api.errors import ValidationError


class Spectra:
    """Entity"""
    def __init__(self, id, name, data):
        self._id = id
        self.name = name
        self.data = SpectraData(data)

    @property
    def id(self):
        """read only"""
        return self._id

    def truncate(self, start: int, end: int):
        self.data.truncate(start, end)


class MixedSpectra(Spectra):
    """Entity"""
    def __init__(self, id, name, data, component_ids=None):
        super().__init__(id, name, data)
        self.component_ids = component_ids
        # access id and timestamp by db generating
        spec_dao = SpectraRepository.SpectraDAO(name=self.name)
        if not self._id:
            self._id = spec_dao.id
        self._timestamp = spec_dao.timestamp

    @property
    def timestamp(self):
        return self._timestamp

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'data': self.data.data,
            'timestamp': self.timestamp
        }

    @staticmethod
    def from_json(json_spectra):
        name = json_spectra.get('name')
        if name is None or name == '':
            raise ValidationError('json does not have a name')
        data = json_spectra.get('data')
        if data is None or data == '':
            raise ValidationError('json does not have a data')
        return MixedSpectra(None, name, data)


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
    def __init__(self, id, name, comp_spectras, formula=None):
        super().__init__()
        self._id = id if id else self._generate_id()
        self.name = name
        self.comp_spectras = comp_spectras
        self.formula = formula
        self.state = None
        self.network = None

    def _generate_id(self):
        return ComponentRepository.ComponentDAO(name=self.name, formula=self.formula).id

    @property
    def id(self):
        return self._id

    def is_existing_on(self, spec: Spectra):
        if not self.network:  # lazy load
            self.network = DetectionNetwork(self.id)
            self.network.register(self)
        pass

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
            'data': self.comp_spectras
        }

    @staticmethod
    def from_json(json_spectra):
        name = json_spectra.get('name')
        if name is None or name == '':
            raise ValidationError('json does not have a name')
        data = json_spectra.get('data')
        if data is None or data == '':
            raise ValidationError('json does not have a data')
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

    def predict(self, spec: Spectra):
        pass

    def fit(self, train_data):
        self.state_watcher.busy()
        # fit data
        self.model.fit(train_data.xs, train_data.ys)
        self.state_watcher.online()


class SpectraData:
    """Value object"""
    def __init__(self, data):
        import numpy as np
        if not isinstance(data, (list, tuple, np.ndarray)):
            raise ValueError('spectra data expect list/tuple/np.ndarray but get {}'.format(type(data)))
        data_array = np.array(data)
        if not data_array.ndim == 2 and data_array.shape[1] == 2:
            raise ValueError('spectra data shape is not correct: {}'.format(data_array.shape))
        self.data = np.array(data)

    def truncate(self, start, end):
        return SpectraData(self.data[start:end])



