import tensorflow as tf


class DenoisingAutoEncoder:

    def __init__(self, path):
        # sess and graph must be assigned in flask app
        self.sess = tf.Session()
        self.graph = tf.get_default_graph()
        tf.keras.backend.set_session(self.sess)
        self.model = tf.keras.models.load_model(path)

    def predict(self, xs):
        with self.graph.as_default():
            tf.keras.backend.set_session(self.sess)
            return self.model.predict(xs)


