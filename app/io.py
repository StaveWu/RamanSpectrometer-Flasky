import os
import numpy as np
from .algorithms.detect import TransferredModel


class IO:

    def __init__(self, path=None, ext=None):
        self.path = path
        self.ext = ext

    def _get_pathname(self, name):
        if not self.path:
            raise RuntimeError('path should not be none')
        return os.path.join(self.path, '{}.{}'.format(name, self.ext))

    def read(self, name):
        pass

    def write(self, name, obj):
        pass

    def delete(self, name):
        pass


class ArrayIO(IO):

    def __init__(self, path=None, ext='txt'):
        super().__init__(path, ext)

    def init_app(self, app):
        pass

    def write(self, name, data):
        pathname = self._get_pathname(name)
        with open(pathname, 'w+') as f:
            for row_eles in data:
                for i, col_ele in enumerate(row_eles):
                    f.write('%f' % col_ele)
                    if i < len(row_eles) - 1:
                        f.write('\t')
                f.write('\n')

    def read(self, name):
        pathname = self._get_pathname(name)
        data = []
        with open(pathname, 'r') as f:
            for line in f.readlines():
                s = line.strip().split('\t')
                data.append([float(ele) for ele in s])
        return np.array(data).astype('float')

    def delete(self, name):
        pathname = self._get_pathname(name)
        if os.path.exists(pathname):
            os.remove(pathname)


class SpectrumIO(ArrayIO):

    def init_app(self, app):
        super().init_app(app)
        self.path = app.config['SPECTRA_PATH']


class ComponentIO(ArrayIO):

    def init_app(self, app):
        super().init_app(app)
        self.path = app.config['COMPONENT_PATH']


class ModelIO(IO):

    def __init__(self, path=None, ext='h5'):
        super().__init__(path, ext)

    def init_app(self, app):
        self.path = app.config['MODEL_PATH']

    def read(self, name):
        pathname = self._get_pathname(name)
        return TransferredModel.load(pathname)

    def write(self, name, obj: TransferredModel):
        pathname = self._get_pathname(name)
        obj.save(pathname)

    def delete(self, name):
        pathname = self._get_pathname(name)
        if os.path.exists(pathname):
            os.remove(pathname)

