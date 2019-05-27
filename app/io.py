import os
import numpy as np


class IO:
    def __init__(self, path=None):
        self.path = path

    @staticmethod
    def init_app(app):
        pass

    def _get_pathname(self, name):
        if not self.path:
            raise RuntimeError('path should not be none')
        return os.path.join(self.path, '{}.txt'.format(name))

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


class SpectrumIO(IO):

    def init_app(self, app):
        IO.init_app(app)
        self.path = app.config['SPECTRA_PATH']


class ComponentIO(IO):

    def init_app(self, app):
        IO.init_app(app)
        self.path = app.config['COMPONENT_PATH']

