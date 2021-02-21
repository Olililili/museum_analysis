import unittest
from unittest.mock import MagicMock
from src.correlate_pop_visitor import calculate_coefficient_and_intercept


class TestCorrelatePopVisitor(unittest.TestCase):
    def test_correlate_pop_visitor(self):
        mocked_model = type('', (), {})()
        mocked_model.coef_ = MagicMock(return_value=[[1]])
        mocked_model.intercept_ = MagicMock(return_value=[2])
        self.assertEqual(2, len(calculate_coefficient_and_intercept(mocked_model)))