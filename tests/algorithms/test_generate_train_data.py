from unittest import TestCase
import pandas as pd
import numpy as np
from app.algorithms.data_generation import generate_train_data


class TestGenerate_train_data(TestCase):

    def setUp(self) -> None:
        df = pd.DataFrame(index=np.linspace(1, 500, 1000),
                          data=np.array([np.linspace(1, 500, 1000), np.linspace(1, 500, 1000)]).T)
        self.df_list = [df for _ in range(4)]

    def test_generate_train_data(self):
        res = generate_train_data(self.df_list)
