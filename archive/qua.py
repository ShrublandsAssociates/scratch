def initialize(context):

    fetch_csv('https://dl.dropboxusercontent.com/u/454411527/WFC.csv', date_column = 'date', date_format = '%m/%d/%y')
    fetch_csv('https://dl.dropboxusercontent.com/u/454411527/JPM.csv', date_column = 'date', date_format = '%m/%d/%y')
    fetch_csv('https://dl.dropboxusercontent.com/u/454411527/C.csv', date_column = 'date', date_format = '%m/%d/%y')
    fetch_csv('https://dl.dropboxusercontent.com/u/454411527/GS.csv',date_column = 'date', date_format = '%m/%d/%y')
    fetch_csv('https://dl.dropboxusercontent.com/u/454411527/BAC.csv', date_column = 'date', date_format = '%m/%d/%y')

    context.stock1 = symbol('JPM')
    context.stock2 = symbol('WFC')
    context.stock3 = symbol('C')
    context.stock4 = symbol('GS')
    context.stock5 = symbol('BAC')

    context.security_list = [context.stock1, context.stock2, context.stock3, context.stock4, context.stock5]
    context.MeanEq = -6.36/np.power(10, 6)
    context.SDEq = 0.0444
    context.Weights = [-0.008867356, -0.006111029, -0.008740114, -0.011883530, -0.001827392]
    nWeights = []
    for weight in context.Weights:
        nWeights.append(weight*100/sum(context.Weights))
    context.NormalizedWeights = nWeights
    context.in_high = False
    context.in_low = False
    schedule_function(rebalance, date_rule=date_rules.every_day(), time_rule=time_rules.market_close(hours=1))
def rebalance(context, data):
    if len(get_open_orders()) > 0:
        return
    s1 = context.stock1
    s2 = context.stock2
    s3 = context.stock3
    s4 = context.stock4
    s5 = context.stock5
    #bestFit = context.Weights[1]*s1
    #print bestFit
    #p50 = data.history(context.security_list, 'price', 50, '1d')
    closing_price = data.history(context.security_list, 'price', 1, '1d')
    #p10 = p50.iloc[-10:]
    print closing_price
    bestFit = context.Weights[0]*data.current('RDA', 'Residuals') + context.Weights[1]*data.current(context.stock2, 'Residuals') + context.Weights[2]*data.current(context.stock3, 'Residuals') + context.Weights[3]*data.current(context.stock4, 'Residuals') + context.Weights[4]*data.current(context.stock5, 'Residuals')
    print bestFit
    # Get the 50 day mavg
    #m50 = np.mean(p50[s2] - p50[s3])
    # Get the std of the last 60 days
    #std50 = np.std(p50[s2] - p50[s3])
    # Current diff = 5 day mavg
    #m10 = np.mean(p10[s2] - p10[s3])
    # Compute z-score
    #if std50 > 0:
    #    zscore = (m10 - m50)/std50
    #else:
    #   zscore = 0
    #, style=StopLimitOrder(limit_price = closing_price[s2][0]*1.01, stop_price=closing_price[s2][0]*1.01)
    if bestFit > context.SDEq and not context.in_high and all(data.can_trade(context.security_list)):
        order_target_percent(s1, -context.NormalizedWeights[0],limit_price = closing_price[s2][0]*1.01,stop_price=closing_price[s1][0]*1.01)
        order_target_percent(s2, -context.NormalizedWeights[1],limit_price = closing_price[s2][0]*1.01,stop_price=closing_price[s2][0]*1.01)
        order_target_percent(s3, -context.NormalizedWeights[2],limit_price = closing_price[s2][0]*1.01,stop_price=closing_price[s3][0]*1.01)
        order_target_percent(s4, -context.NormalizedWeights[3],limit_price = closing_price[s2][0]*1.01,stop_price=closing_price[s4][0]*1.01)
        order_target_percent(s5, -context.NormalizedWeights[4],limit_price = closing_price[s2][0]*1.01,stop_price=closing_price[s5][0]*1.01)
        context.in_high = True
        context.in_low = False
    elif bestFit < -context.SDEq and not context.in_low and all(data.can_trade(context.security_list)):
        order_target_percent(s1, context.NormalizedWeights[0],stop_price=closing_price[s1][0]*1.01)
        order_target_percent(s2, context.NormalizedWeights[1],stop_price=closing_price[s1][0]*1.01)
        order_target_percent(s3, context.NormalizedWeights[2],stop_price=closing_price[s1][0]*1.01)
        order_target_percent(s4, context.NormalizedWeights[3],stop_price=closing_price[s1][0]*1.01)
        order_target_percent(s5, context.NormalizedWeights[4],stop_price=closing_price[s1][0]*1.01)
        context.in_high = False
        context.in_low = True
    elif abs(bestFit) < context.MeanEq  and all(data.can_trade(context.security_list)):
        order_target_percent(s1, 0)
        order_target_percent(s2, 0)
        order_target_percent(s3, 0)
        order_target_percent(s4, 0)
        order_target_percent(s5, 0)
        context.in_high = False
        context.in_low = False
    record('bestFit', bestFit, lev=context.account.leverage)