import numpy as np


def to_input_shape(xs, size):
    if xs.shape[1] == size:
        return xs
    elif xs.shape[1] < size:
        # fill zeros in the end of xs
        return np.array([list(x) + [0] * (size - len(x)) for x in xs])
    else:
        return xs[:, :size]