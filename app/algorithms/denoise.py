from scipy.signal import savgol_filter
import numpy as np
from .utils import to_input_shape
import os
from .dae import DenoisingAutoEncoder


# if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
basedir = os.path.abspath(os.path.dirname(__file__))
dae_model = DenoisingAutoEncoder('{}/dae.h5'.format(basedir))


def dae(x):
    x = np.array(x)
    dims = x.ndim
    if dims > 2:
        raise ValueError('expect input ndim <= 2 but get {} dims'.format(dims))
    if x.ndim == 1:
        x = x.reshape(1, -1)
    features = x.shape[1]
    x = to_input_shape(x, 3000)
    x = np.expand_dims(x, axis=2)

    res = dae_model.predict(x)

    res = np.squeeze(res, axis=2)
    res = to_input_shape(res, features)
    return res if dims == 2 else res.flatten()


def wavelet(x):
    pass

