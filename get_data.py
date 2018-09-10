import tushare as ts
import pandas as pd
import os

ts.set_token('ae26b6dc28d7f0a3e4bfc10cdccf39591dd4768de8a2f767cdb0a93e')
pro = ts.pro_api()

#ZZ500 = pd.read_csv('./ZZ500/ZZ500.csv', encoding='gb18030')
HS300 = pd.read_csv('./HS300/HS300.csv', encoding='gb18030')


def calendar(startdate, enddate):
    result = pro.trade_cal(exchange_id='', start_date=startdate, end_date=enddate, field='pretrade_date', is_open='1')
    return result


def get_price(startdate, enddate):
    price_data = pd.DataFrame([])
    temp_price = pd.DataFrame([])
    i = 1
    #for symbol in ZZ500['Code']:
    for symbol in HS300['Code']:
        print('get price data from ' + startdate + ' to ' + enddate + ': ' + str(i / 300) + '%')
        temp_price = pro.daily(ts_code=symbol, start_date=startdate, end_date=enddate)
        price_data = price_data.append(temp_price)
        i = i + 1
    price_data = price_data.sort_values(by=['trade_date', 'ts_code'], axis=0, ascending=False)
    if os.path.exists('../RawData/price_data.csv'):
        price_data.to_csv('../RawData/price_data.csv', mode='a', header=None)
    else:
        price_data.to_csv('../RawData/price_data.csv')
    return price_data


def get_price_adj():
    temp_adj = pd.DataFrame([])
    price_adj_factor = pd.DataFrame([])
    i = 1
    #for symbol in ZZ500['Code']:
    for symbol in HS300['Code']:
        print('get price adjust factor: ' + str(i / 300) + '%')
        temp_adj = pro.adj_factor(ts_code=symbol)
        price_adj_factor = price_adj_factor.append(temp_adj)
        i = i + 1
    price_adj_factor = price_adj_factor.sort_values(by=['trade_date', 'ts_code'], axis=0, ascending=False)
    if os.path.exists('../RawData/price_adj_factor.csv'):
        price_adj_factor.to_csv('../RawData/price_adj_factor.csv', mode='a', header=None)
    else:
        price_adj_factor.to_csv('../RawData/price_adj_factor.csv')
    return price_adj_factor


def get_basic(startdate, enddate):
    daily_basic = pd.DataFrame([])
    temp_basic = pd.DataFrame([])
    i = 1
    #for symbol in ZZ500['Code']:
    for symbol in HS300['Code']:
        print('get daily basic data from ' + startdate + 'to ' + enddate + ': ' + str(i / 300) + '%')
        temp_basic = pro.daily_basic(ts_code=symbol, start_date=startdate, end_date=enddate)
        daily_basic = daily_basic.append(temp_basic)  # 需要去除休假日，和交易日join
        i = i + 1
    daily_basic = daily_basic.sort_values(by=['trade_date', 'ts_code'], axis=0, ascending=False)
    if os.path.exists('../RawData/daily_basic.csv'):
        daily_basic.to_csv('../RawData/daily_basic.csv', mode='a', header=None)
    else:
        daily_basic.to_csv('../RawData/daily_basic.csv')
    return daily_basic


def get_suspend():
    suspend = pd.DataFrame([])
    temp_suspend = pd.DataFrame([])
    i = 1
    #for symbol in ZZ500['Code']:
    for symbol in HS300['Code']:
        print('get suspend data: ' + str(i / 300) + '%')
        temp_suspend = pro.suspend(ts_code=symbol)
        suspend = suspend.append(temp_suspend)
        i = i + 1
    suspend = suspend.sort_values(by=['suspend_date', 'ts_code'], axis=0, ascending=False)
    if os.path.exists('../RawData/suspend.csv'):
        suspend.to_csv('../RawData/suspend.csv', mode='a', header=None, encoding='gbk')
    else:
        suspend.to_csv('../RawData/suspend.csv', encoding='gbk')
    return suspend


def get_financial_indicators(startdate, enddate):  # max year = 7
    financial_indicator = pd.DataFrame([])
    temp_FI = pd.DataFrame([])
    i = 1
    #for symbol in ZZ500['Code']:
    for symbol in HS300['Code']:
        print('get financial indicators from ' + startdate + 'to ' + enddate + ': ' + str(i / 300) + '%')
        temp_FI = pro.fina_indicator(ts_code=symbol, start_date=startdate, end_date=enddate)
        financial_indicator = financial_indicator.append(temp_FI)
        i = i + 1
    financial_indicator = financial_indicator.sort_values(by=['ann_date', 'ts_code'], axis=0, ascending=False)
    if os.path.exists('../RawData/financial_indicator.csv'):
        financial_indicator.to_csv('../RawData/financial_indicator.csv', mode='a', header=None)
    else:
        financial_indicator.to_csv('../RawData/financial_indicator.csv')
    return financial_indicator
