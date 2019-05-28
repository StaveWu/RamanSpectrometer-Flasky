from unittest import TestCase
from app.algorithms.data_generation import ConcentrationRoller


class TestConcentrationRoller(TestCase):
    def setUp(self) -> None:
        self.roller = ConcentrationRoller(1, 1000, 2)

    def test_roll_unique(self):
        res = []
        for i in range(10):
            res.append(self.roller.roll_unique(1))
        print(res)
