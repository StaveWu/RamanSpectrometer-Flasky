from unittest import TestCase
import pandas as pd
import numpy as np
from app.algorithms.data_generation import scale_dataframe


class TestScale_dataframe(TestCase):
    def test_scale_dataframe(self):
        df = pd.DataFrame(index=[1, 2, 4], data=np.array([[1, 2], [2, 2], [4, 2]]), columns=['a', 'b'])
        print(scale_dataframe(df))
