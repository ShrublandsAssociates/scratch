def run_test(context, stock_data, func):
    for index in stock_data.index:
        func(context, stock_data.loc[index], index)
