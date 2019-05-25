import os
import numpy as np


class SpectrumIO:
    def __init__(self, path):
        self.path = path

    def write(self, id, data):
        pathname = os.path.join(self.path, id)
        with open(pathname, 'w') as f:
            for row_eles in data:
                for i, col_ele in enumerate(row_eles):
                    f.write('%f' % col_ele)
                    if i < len(row_eles) - 1:
                        f.write('\t')
                f.write('\n')

    def read_by_id(self, id):
        pathname = os.path.join(self.path, id)
        data = []
        with open(pathname, 'r') as f:
            for line in f.readlines():
                s = line.strip().split('\t')
                data.append([float(ele) for ele in s])
        return np.array(data).astype('float')

    def delete_by_id(self, id):
        pathname = os.path.join(self.path, id)
        if os.path.exists(pathname):
            os.remove(pathname)


spectrum_io = SpectrumIO(path='')
component_io = SpectrumIO(path='')
