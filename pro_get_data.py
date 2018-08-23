import tushare as ts
import pandas as pd

###########连接
from pandas import DataFrame

ts.set_token('ae26b6dc28d7f0a3e4bfc10cdccf39591dd4768de8a2f767cdb0a93e')
pro = ts.pro_api()


###########获取交易日历及所有股票
calendar = pro.trade_cal(exchange_id='',start_date='20180810',end_date='20180820',field='pretrade_date',is_open='1')
stock_pool = pro.stock_basic(exchange_id='',fields='symbol,name,list_date,list_status')


###########提取日线、复权因子、是否停牌
price_data = pd.DataFrame([])
price_adj_factor = pd.DataFrame([])
suspend = pd.DataFrame([])
daily_basic: DataFrame = pd.DataFrame([])
for date in calendar['cal_date']:
    temp_price = pro.daily(trade_date=date)
    temp_adj = pro.adj_factor( trade_date=date)
    temp_suspend = pro.suspend(suspend_date=date)
    temp_basic = pro.daily_basic(ts_code='', trade_date=date)
    print('now get data on '+date)
    price_data=price_data.append(temp_price)
    price_adj_factor=price_adj_factor.append(temp_adj)
    suspend = suspend.append(temp_suspend)
    daily_basic = daily_basic.append(temp_basic)

###########财务数据

income_statement=pd.DataFrame([])
balance_sheet=pd.DataFrame([])
cashflow_statement=pd.DataFrame([])
for symbol in stock_pool['symbol'].head(5):
    print('now get the stock '+ symbol)
    if int(symbol) < 600000:
        temp_is = pro.income(ts_code=str(symbol)+'.SZ', start_date='20180110', end_date='20180730')
        temp_bs = pro.balancesheet(ts_code = str(symbol)+'.SZ', start_date='20180101', end_date='20180730')
        temp_cs = pro.cashflow(ts_code=str(symbol)+'.SZ', start_date='20180101', end_date='20180730')
    else:
        temp_is = pro.income(ts_code=str(symbol) + '.SH', start_date='20180110')
        temp_bs = pro.balancesheet(ts_code = str(symbol)+'.SH', start_date='20180101', end_date='20180730')
        temp_cs = pro.cashflow(ts_code=str(symbol)+'.SH', start_date='20180101', end_date='20180730')
    income_statement=income_statement.append(temp_is)
    balance_sheet=balance_sheet.append(temp_bs)
    cashflow_statement=cashflow_statement.append(temp_cs)
