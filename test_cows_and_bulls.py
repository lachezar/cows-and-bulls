import unittest
import cows_and_bulls

class TestCowsAndBulls(unittest.TestCase):

    def setUp(self):
        self.cnb = cows_and_bulls.Game()

    def test_contrain(self):
        self.cnb.possible_numbers = ((1,2,3,4), (1,2,3,5), (1,2,3,6), (7,8,9,0), (1,2,5,6))
        result = self.cnb.constrain((1,2,5,6), {'cows': 1, 'bulls': 2})
        self.assertEquals(result, ((1,2,3,5),))

if __name__ == '__main__':
    unittest.main()
    