def calc(open_positions, prices):
    profit_loss = 0
    for open_position in open_positions:
        profit_loss += open_position.get_current_value(prices[open_position.symbol]) - open_position.get_order_value()

    return profit_loss
