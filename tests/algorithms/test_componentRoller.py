from unittest import TestCase
from app.algorithms.data_generation import ComponentRoller
import pandas as pd
import numpy as np


class TestComponentRoller(TestCase):

    def setUp(self) -> None:
        df1 = pd.DataFrame(index=[1, 2, 4], data=np.array([[1, 2], [1, 2], [1, 2]]))
        df2 = pd.DataFrame(index=[1, 2, 4], data=np.array([[3, 4], [3, 4], [3, 4]]))
        self.roller = ComponentRoller([df1, df2], 1)

    def test_roll(self):
        print(self.roller.roll())
