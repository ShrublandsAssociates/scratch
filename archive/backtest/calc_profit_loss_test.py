import unittest
from calc_profit_loss import calc
from order import Order

class TestCalcProfitLoss(unittest.TestCase):

    def test_should_be_zero_with_no_open_positions(self):
        self.assertEqual(calc([], {}), 0)

    def test_should_be_correct_with_single_order(self):
        open_positions = [ Order(100, 120, 'FB'), Order(100, 120, 'FB') ]
        self.assertEqual(calc(open_positions, { 'FB': 130 }), 2000)

    def test_should_be_correct_with_multiple_orders_of_same_stock(self):
        open_positions = [ Order(100, 120, 'FB'), Order(100, 135, 'FB') ]
        self.assertEqual(calc(open_positions, { 'FB': 130 }), 500)

    def test_error_if_stock_price_is_unknown(self):
        open_positions = [ Order(100, 120, 'IBM') ]
        self.assertRaises(KeyError, calc, open_positions, {})

if __name__ == '__main__':
    unittest.main()
