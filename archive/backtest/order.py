""" Stock Order """
class Order:
    """ Stock Order """

    def __init__(self, amount, price, symbol):
        self.amount = amount
        self.price = price
        self.symbol = symbol

    def get_order_value(self):
        """ Cost of this order """
        return self.count * self.price

    def get_current_value(self, price):
        """ Price of this order base on current stock price """
        return price * self.count
