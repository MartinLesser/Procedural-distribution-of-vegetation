import unittest
from intern.src.python.Logic.probabilities import Probabilities


class TestProbabilitiesClass(unittest.TestCase):

    def test_CalculateProbabilityAvailableBelowNeeded(self):
        # given
        needed_calories = 40
        available_calories = [0, 10, 20, 30, 40]
        expected = [0.0, 0.25, 0.5, 0.75, 1.0]

        for i in range(len(available_calories)):
            # when
            probability = Probabilities.calculate_probability(needed_calories, available_calories[i])

            # then
            self.assertEqual(probability, expected[i])

    def test_CalculateProbabilityAvailableAboveNeeded(self):
        # given
        needed_calories = 40
        available_calories = [50, 60, 70, 80, 90]
        expected = [0.75, 0.5, 0.25, 0.0, 0.0]

        for i in range(len(available_calories)):
            # when
            probability = Probabilities.calculate_probability(needed_calories, available_calories[i])

            # then
            self.assertEqual(probability, expected[i])


if __name__ == '__main__':
    unittest.main()
