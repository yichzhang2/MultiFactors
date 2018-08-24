import tushare as ts
import pandas as pd

ts.set_token('ae26b6dc28d7f0a3e4bfc10cdccf39591dd4768de8a2f767cdb0a93e')
pro = ts.pro_api()

ZZ500=pd.read_csv('./ZZ500/ZZ500.csv',encoding = 'gb18030')

def calendar(startdate,enddate):
    result = pro.trade_cal(exchange_id='',start_date=startdate,end_date=enddate,field='pretrade_date',is_open='1')
    return result

def get_price(startdate,enddate):
    price_data = pd.DataFrame([])
    price_adj_factor = pd.DataFrame([])

    for symbol in ZZ500['Code'].head(5):
        try:
            print('handling stock '+symbol)
            temp_price = pro.daily(ts_code=symbol, start_date=startdate,end_date=enddate)
            temp_adj = pro.adj_factor(ts_code=symbol)
        except:
            pass
        price_data = price_data.append(temp_price)
        price_adj_factor = price_adj_factor.append(temp_adj)

    price_adj_factor.to_csv('../RawData/price_adj_factor.csv')
    price_data.to_csv('../RawData/price_data.csv')

    return price_adj_factor,price_data

def get_basic(startdate,enddate):
    suspend = pd.DataFrame([])
    daily_basic = pd.DataFrame([])
    for symbol in ZZ500['Code'].head(5):
        print('handling stock ' + symbol)
        temp_suspend = pro.suspend(ts_code=symbol)
        temp_basic = pro.daily_basic(ts_code=symbol, start_date=startdate,end_date=enddate)
        suspend = suspend.append(temp_suspend)
        daily_basic = daily_basic.append(temp_basic) # 需要去除休假日，和交易日join

    daily_basic.to_csv('../RawData/daily_basic.csv')
    suspend.to_csv('../RawData/suspend.csv',encoding = 'gb18030')
    return daily_basic,suspend

def get_financial_indicators(startdate,enddate):    # max year = 7
    financial_indicator = pd.DataFrame([])
    for symbol in ZZ500['Code'].head(5):
        print('handling stock ' + symbol)
        temp_FI = pro.fina_indicator(ts_code=symbol, start_date=startdate, end_date=enddate)
        financial_indicator = financial_indicator.append(temp_FI)
    financial_indicator.to_csv('../RawData/financial_indicator.csv')
    return  financial_indicator