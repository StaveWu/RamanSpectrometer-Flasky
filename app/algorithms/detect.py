from tensorflow import keras
from sklearn.preprocessing import minmax_scale
from sklearn.utils import shuffle
import numpy as np
from .debackground import airPLS
from .denoise import dae
from .utils import to_input_shape
import tensorflow as tf


class Model:
    def __init__(self):
        # hack code, to make sure model running without error on multi-thread app
        self.sess = tf.Session()
        self.graph = tf.get_default_graph()
        tf.keras.backend.set_session(self.sess)

    def predict(self, xs):
        pass

    def fit(self, xs, ys, batch_size, epochs):
        pass

    def save(self, path):
        pass


def _pre_process(xs):
    xs = to_input_shape(xs, 3000)
    # xs = np.array([airPLS(x, lambda_=50) for x in xs])
    xs = minmax_scale(xs, axis=1)
    xs = dae(xs)
    return xs


class MultiTaskModel(Model):
    def __init__(self, path=None, units_output=6):
        super().__init__()
        self.units_output = units_output
        if not path:
            self.model = self._new_model()
            self.trained = False
        else:
            self.model = keras.models.load_model(path)
            self.trained = True

    def _new_model(self):
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
        model.add(keras.layers.Dense(self.units_output, name='last_dense_layer'))
        model.add(keras.layers.Activation('sigmoid'))
        model.summary()

        model.compile(loss=keras.losses.binary_crossentropy,
                      optimizer=keras.optimizers.Adam(),
                      metrics=['accuracy'])
        return model

    @staticmethod
    def _load_model(model_path):
        return MultiTaskModel(model_path)

    def fit(self, xs, ys, batch_size, epochs):
        xs = _pre_process(xs)
        xs, ys = shuffle(xs, ys)
        xs = np.expand_dims(xs, axis=2)
        print('================try fit=================')
        with self.graph.as_default():
            tf.keras.backend.set_session(self.sess)
            self.model.fit(xs, ys, batch_size=batch_size, epochs=epochs)
        self.trained = True

    def predict(self, xs):
        xs = to_input_shape(xs, 3000)
        xs = np.expand_dims(xs, axis=2)
        with self.graph.as_default():
            tf.keras.backend.set_session(self.sess)
            return self.model.predict(xs)

    def save(self, path):
        self.model.save(path)

    def to_transferred_model(self):
        if not self.trained:
            raise RuntimeError('multi-task model has not been trained')
        else:
            convolutional_base = self.model.layers[:-4]
            return TransferredModel(sess=self.sess, graph=self.graph, convolutional_base=convolutional_base)


class TransferredModel(Model):
    def __init__(self, path=None, sess=None, graph=None, convolutional_base=None):
        super().__init__()
        if path:
            self.model = keras.models.load_model(path)
        else:
            if not (sess and graph and convolutional_base):
                raise RuntimeError('transferred model should be given one of path or convolutional base')
            else:
                self.sess = sess
                self.graph = graph
                tf.keras.backend.set_session(self.sess)
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

    def fit(self, xs, ys, batch_size, epochs):
        xs = _pre_process(xs)
        xs, ys = shuffle(xs, ys)
        xs = np.expand_dims(xs, axis=2)
        with self.graph.as_default():
            tf.keras.backend.set_session(self.sess)
            self.model.fit(xs, ys, batch_size=batch_size, epochs=epochs)

    def predict(self, xs):
        xs = to_input_shape(xs, 3000)
        xs = np.expand_dims(xs, axis=2)
        with self.graph.as_default():
            tf.keras.backend.set_session(self.sess)
            return self.model.predict(xs)

    def save(self, path):
        self.model.save(path)

    @staticmethod
    def load(path):
        return TransferredModel(path)


class ModelFactory:

    @staticmethod
    def new_initial_transferred_model(xs, ys):
        multitask_model = MultiTaskModel(units_output=ys.shape[1])
        multitask_model.fit(xs, ys, batch_size=32, epochs=5)
        return multitask_model.to_transferred_model()

    @staticmethod
    def new_multitask_model():
        return MultiTaskModel()


