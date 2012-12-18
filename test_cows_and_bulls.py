import unittest
import cows_and_bulls
from ai import AI

class TestCowsAndBulls(unittest.TestCase):

    def setUp(self):
        self.ai = AI()

    def test_contrain(self):
        self.ai.possible_numbers = ((1,2,3,4), (1,2,3,5), (1,2,3,6), (7,8,9,0), (1,2,5,6))
        result = self.ai.constrain((1,2,5,6), {'cows': 1, 'bulls': 2})
        self.assertEquals(result, ((1,2,3,5),))

if __name__ == '__main__':
    unittest.main()
    