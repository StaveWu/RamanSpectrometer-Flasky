from unittest import TestCase
import pandas as pd
import numpy as np
from app.algorithms.data_generation import alignment


class TestAlignment(TestCase):
    def test_alignment(self):
        df1 = pd.DataFrame(index=[1, 2, 4], data=np.array([[1, 1], [2, 2], [4, 4]]))
        df2 = pd.DataFrame(index=[3, 5, 7], data=np.array([[3, 3], [5, 5], [7, 7]]))
        res = alignment([df1, df2])
        assert all(a == b for a, b in zip(res[0].index, res[1].index))
        assert all(a == b for a, b in zip(res[0].values[:, 0], [1, 2, 2, 4, 4, 4]))
        assert all(a == b for a, b in zip(res[1].values[:, 0], [3, 3, 3, 3, 5, 7]))
