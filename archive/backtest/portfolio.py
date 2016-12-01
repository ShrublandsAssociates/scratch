""" Portfolio """
from calc_profit_loss import calc
from order import Order

class Portfolio:
    """ Portfolio """

    def __init__(self, balance):
        self.balance = balance # Accounts value excluding open position P&L
        self.profit_loss = 0 # Sum of the profit and loss from open positions
        self.open_positions = []

    def get_profit_loss(self, prices):
        return calc(self.open_positions, prices)

    def get_equity(self, prices):
        return self.balance + self.get_profit_loss(prices)

    def place_order(self, amount, price, symbol):
        self.open_positions.append(Order(amount, price, symbol))

    def close_order(self, order, price):
        self.balance += order.get_current_value(price)

    def close_orders(self, price, conditional = lambda x: True):
        new_open_positions = []
        for open_position in self.open_positions:
            if conditional(open_position):
                self.close_order(open_position, price)
            else:
                new_open_positions.append(open_position)
        return new_open_positions
