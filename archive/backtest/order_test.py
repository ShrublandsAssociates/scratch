import unittest
from order import Order

class TestStringMethods(unittest.TestCase):

    def test_get_order_value(self):
        new_order = Order(100, 122, 'FB')
        self.assertEqual(new_order.get_order_value(), 12200)

    def test_symbol(self):
        new_order = Order(100, 122, 'FB')
        self.assertEqual(new_order.symbol, 'FB')

    def test_get_current_value(self):
        new_order = Order(100, 122, 'FB')
        self.assertEqual(new_order.get_current_value(124), 12400)

if __name__ == '__main__':
    unittest.main()
