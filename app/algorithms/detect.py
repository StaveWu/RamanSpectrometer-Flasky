from tensorflow import keras
from sklearn.preprocessing import minmax_scale
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
    else:
        # fill zeros in the end of xs
        return np.array([x + [0] * (3000 - len(x)) for x in xs])


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


def alignment(xs):
    pass


def generate_train_data(comps, concen_upper_bound=1000, num_per_combination=1000):
    pass

