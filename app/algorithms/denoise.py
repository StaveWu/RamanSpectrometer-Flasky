from scipy.signal import savgol_filter
from tensorflow import keras
import numpy as np


def dae(x):
    x = np.array(x)
    dims = x.ndim
    if dims == 1:
        x = x.reshape(-1, 1)
    if dims == 2:
        x = np.expand_dims(x, axis=2)
    model = keras.models.load_model('./dae.h5')
    res = model.predict(x)
    if dims == 2:
        res = np.squeeze(res, axis=2)
    if dims == 1:
        res = res.flatten()
    return res


def wavelet(x):
    pass

