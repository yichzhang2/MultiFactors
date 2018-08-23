import tushare as ts

###########连接
ts.set_token('ae26b6dc28d7f0a3e4bfc10cdccf39591dd4768de8a2f767cdb0a93e')
pro = ts.pro_api()


###########获取交易日历
df = pro.trade_cal(exchange_id='',start_date='20180101',end_date='',field='pretrade_date',is_open='0')
data = pro.stock_basic(exchange_id='',fields='symbol,name,list_date,list_status')