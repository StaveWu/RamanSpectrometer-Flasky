from tensorflow import keras
from sklearn.preprocessing import minmax_scale, normalize, scale
from sklearn.utils import shuffle
import numpy as np
from .debackground import airPLS
from .denoise import dae


class Model:
    def predict(self, xs):
        pass

    def fit(self, xs, ys):
        pass

    def save(self, path):
        pass


def _to_input_shape(xs):
    if xs.shape[1] == 3000:
        return xs
    elif xs.shape[1] < 3000:
        # fill zeros in the end of xs
        return np.array([x + [0] * (3000 - len(x)) for x in xs])
    else:
        return xs[:, :3000]


def _pre_process(xs):
    xs = _to_input_shape(xs)
    xs = np.array([airPLS(x, lambda_=50) for x in xs])
    xs = minmax_scale(xs, axis=1)
    return dae(xs)


class MultiTaskModel(Model):
    def __init__(self, path=None):
        if not path:
            self.model = self._new_model()
            self.trained = False
        else:
            self.model = self._load_model(path)
            self.trained = True

    @staticmethod
    def _new_model():
        model = keras.models.Sequential()
        model.add(keras.layers.LocallyConnected1D(32, 11, strides=5, activation='relu', name='first_conv_layer',
                                                  kernel_constraint=keras.constraints.min_max_norm(),
                                                  input_shape=(3000, 1)))
        model.add(keras.layers.Conv1D(32, 3, activation='relu'))
        model.add(keras.layers.Conv1D(32, 3, activation='relu'))
        model.add(keras.layers.MaxPool1D())
        model.add(keras.layers.Conv1D(32, 3, activation='relu'))
        model.add(keras.layers.Conv1D(32, 3, activation='relu'))
        model.add(keras.layers.MaxPool1D())
        model.add(keras.layers.Conv1D(32, 3, activation='relu'))
        model.add(keras.layers.Conv1D(32, 3, activation='relu', name='last_conv_layer'))
        model.add(keras.layers.MaxPool1D())
        model.add(keras.layers.Flatten())
        model.add(keras.layers.Dropout(0.5))
        model.add(keras.layers.Dense(64, activation='relu'))
        model.add(keras.layers.Dense(16, activation='relu'))
        model.add(keras.layers.Dense(6, name='last_dense_layer'))
        model.add(keras.layers.Activation('sigmoid'))
        model.summary()

        model.compile(loss=keras.losses.binary_crossentropy,
                      optimizer=keras.optimizers.Adam(),
                      metrics=['accuracy'])
        return model

    @staticmethod
    def _load_model(model_path):
        return keras.models.load_model(model_path)

    def fit(self, xs, ys):
        xs = _pre_process(xs)
        shuffle(xs, ys)
        xs = np.expand_dims(xs, axis=2)
        self.model.fit(xs, ys)

    def predict(self, xs):
        return self.model.predict(xs)

    def save(self, path):
        self.model.save(path)

    def to_transferred_model(self):
        if not self.trained:
            raise RuntimeError('multi-task model is not trained')
        else:
            return TransferredModel(convolutional_base=self.model.layers)


class TransferredModel(Model):
    def __init__(self, path=None, convolutional_base=None):
        if path:
            self.model = keras.models.load_model(path)
        else:
            if not convolutional_base:
                raise RuntimeError('transferred model should be given one of path or convolutional base')
            else:
                for layer in convolutional_base:
                    layer.trainable = False
                self.model = keras.models.Sequential(convolutional_base)
                self.model.add(keras.layers.Dense(64, activation='relu'))
                self.model.add(keras.layers.Dense(16, activation='relu'))
                self.model.add(keras.layers.Dense(1, name='last_dense_layer'))
                self.model.add(keras.layers.Activation('sigmoid'))
                self.model.summary()

                self.model.compile(loss=keras.losses.binary_crossentropy,
                                   optimizer=keras.optimizers.Adam(lr=1e-5),
                                   metrics=['accuracy'])

    def fit(self, xs, ys):
        xs = _pre_process(xs)
        shuffle(xs, ys)
        xs = np.expand_dims(xs, axis=2)
        self.model.fit(xs, ys)

    def predict(self, xs):
        return self.model.predict(xs)

    def save(self, path):
        self.model.save(path)

    @staticmethod
    def load(path):
        return keras.models.load_model(path)


class ModelFactory:

    @staticmethod
    def new_initial_transferred_model(xs, ys):
        multitask_model = MultiTaskModel()
        multitask_model.fit(xs, ys)
        return multitask_model.to_transferred_model()

    @staticmethod
    def new_multitask_model():
        return MultiTaskModel()


import pandas as pd
from typing import List


class ComponentRoller:
    def __init__(self, comps: List[pd.DataFrame], roll_size):
        self.comps = comps
        self.roll_size = roll_size

    def count(self):
        return len(self.comps)

    def roll(self):
        picked_id = np.random.choice(self.count(), self.roll_size, replace=False)
        picked_comps = []
        for i in picked_id:
            c = self.comps[i]
            r = np.random.randint(c.shape[1])
            picked_comps.append(c.iloc[:, r])

        mask = np.zeros(self.count())
        for i in picked_id:
            mask[i] = 1
        # translate hot bit to num.
        # i.e. [1, 1, 0, 0] will be coded as 12
        from functools import reduce
        label = reduce(lambda x, y: x * 2 + y, mask)
        label = label.astype('int')

        df = pd.concat(picked_comps, axis=1)
        return df.values, label


class ConcentrationRoller:
    def __init__(self, lower_bound, upper_bound, roll_size):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.roll_size = roll_size
        self.roll_history = {}

    def roll_unique(self, label):
        vector = np.random.choice(np.arange(self.lower_bound, self.upper_bound, 1), self.roll_size)
        vector_normed = normalize(vector.reshape(1, -1)).flatten()
        return vector_normed if self._add_to_history(label, vector_normed) else self.roll_unique(label)

    def _add_to_history(self, label, vector):
        if label not in self.roll_history:
            self.roll_history[label] = set()
        prev_count = len(self.roll_history[label])
        self.roll_history[label].add(tuple(vector))
        cur_count = len(self.roll_history[label])
        return cur_count != prev_count


def generate_train_data(comps: List[pd.DataFrame], concen_upper_bound=1000, num_per_combination=1000):
    cps = [_to_int_index(c) for c in comps]
    cps = _alignment(cps)
    cps = _scale(cps)

    samples = []
    for n_class in range(1, len(cps) + 1):
        comps_roller = ComponentRoller(cps, n_class)
        concen_roller = ConcentrationRoller(1, concen_upper_bound, n_class)
        for i in range(num_per_combination):
            picked_comps, label = comps_roller.roll()
            concen_vector = concen_roller.roll_unique(label)
            the_sample = pd.Series(name=label, data=np.sum(picked_comps * concen_vector, axis=0))
            samples.append(the_sample)
            if i % 100 == 0:
                print('组合数%d: 第%d个样本 --- 标签%d，浓度比%s' % (n_class, i, label, concen_vector))
        df = pd.concat(samples, axis=1)
        return df.values.T, df.columns.tolist()


def _to_int_index(df: pd.DataFrame):
    index = np.array(df.index).round()
    data = df.values
    data_average = np.array([np.mean(d, axis=1) for d in _split_by_duplicate_index(index, data)])
    return pd.DataFrame(index=set(index), data=data_average)


def _split_by_duplicate_index(index, data):
    if len(index) != len(data):
        raise ValueError('expect the same length')
    res = []
    group = [data[0]]
    for i in range(1, len(index)):
        if index[i] != index[i - 1]:
            res.append(group)
        else:
            group.append(data[i])
    res.append(group)
    return res


def _alignment(dfs: List[pd.DataFrame]):
    grid = [df.shape[1] for df in dfs]
    df = pd.concat(dfs, axis=1)
    df = df.fillna(method='ffill')
    df = df.fillna(method='bfill')
    res = []
    pt = 0
    for g in grid:
        res.append(df.iloc[:, pt:pt+g])
        pt += g
    return res


def _scale(dfs: List[pd.DataFrame]):
    return [pd.DataFrame(data=scale(df.values), columns=df.columns) for df in dfs]



