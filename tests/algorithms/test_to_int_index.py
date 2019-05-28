from unittest import TestCase
import pandas as pd
import numpy as np
import pytest
from app.algorithms.data_generation import to_int_index, split_by_duplicate_index


class TestTo_int_index(TestCase):

    def test_to_int_index(self):
        s1 = pd.Series(index=[1.1, 2.2, 3.3], data=[2, 3, 4], name='a')
        s2 = pd.Series(index=[1.1, 2.2, 3.3], data=[2, 3, 4], name='b')
        df = pd.concat([s1, s2], axis=1)
        df = to_int_index(df)
        assert df.shape == (3, 2)

        s1 = pd.Series(index=[1.1, 2.7, 3.3], data=[2, 3, 4], name='a')
        s2 = pd.Series(index=[1.1, 2.7, 3.3], data=[2, 1, 5], name='b')
        df = pd.concat([s1, s2], axis=1)
        df = to_int_index(df)
        assert df.shape == (2, 2)

    def test_split_by_duplicate_index(self):
        index = [1, 1, 2, 3, 3, 3]
        data = np.array([[1, 1], [1, 1], [2, 2], [3, 3], [3, 3], [3, 3]])
        res = split_by_duplicate_index(index, data)
        assert len(res) == 3
        assert len(res[0]) == 2
        assert len(res[1]) == 1
        assert len(res[2]) == 3

        index = [1, 1, 2]
        with pytest.raises(ValueError):
            split_by_duplicate_index(index, data)


