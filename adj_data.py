import get_data as gd
import pandas as pd
import numpy as np

# gd.get_price_adj()
# gd.get_suspend()
#
# gd.get_price('20170101', '20180824')
# gd.get_price('20140101', '20161231')
# gd.get_price('20110101', '20131231')
#
# gd.get_basic('20170101', '20180824')
# gd.get_basic('20170101', '20180824')
# gd.get_basic('20170101', '20180824')
#
# gd.get_financial_indicators('20170101', '20180824')
# gd.get_financial_indicators('20170101', '20180824')
# gd.get_financial_indicators('20170101', '20180824')

price = pd.read_csv('../RawData/price_data.csv')
price_adj = pd.read_csv('../RawData/price_adj_factor.csv')
basic = pd.read_csv('../RawData/daily_basic.csv')
ZZ500 = pd.read_csv('./ZZ500/ZZ500.csv', encoding='gb18030')
# financial_indicator = pd.read_csv('../RawData/financial_indicator.csv')

temp = price.merge(basic, how='left', on=['ts_code', 'trade_date'])
temp = temp.merge(price_adj, how='left', on=['ts_code', 'trade_date'])

ZZ500.rename(columns={'Code': 'ts_code'}, inplace=True)
temp = temp.merge(ZZ500[['ts_code', 'Industry']], how='left', on='ts_code')
temp = temp.sort_values(by=['trade_date', 'ts_code'], axis=0, ascending=True)

temp = temp.drop(columns=['Unnamed: 0_x', 'Unnamed: 0_y', 'Unnamed: 0', 'volume_ratio','close_y'])
temp.rename(columns={'close_x': 'close'}, inplace=True)
#temp.set_index(['trade_date'],inplace=True) #不一定好
#temp.reset_index(drop=True)

temp['adj_open']=temp['open']*temp['adj_factor']
temp['adj_high']=temp['high']*temp['adj_factor']
temp['adj_low']=temp['low']*temp['adj_factor']
temp['adj_close']=temp['close']*temp['adj_factor']

predict_window=10
for symbol in ZZ500['ts_code']:
    print('solving '+symbol)
    temp_pct=temp[temp['ts_code']==symbol]['adj_close'].pct_change(periods=predict_window)
    temp_date = temp[temp['ts_code'] == symbol]['trade_date']

    temp_shift=temp_pct.shift(-1*predict_window)
    temp_shift = pd.DataFrame({'trade_date': temp_date, 'adj_pct_change': temp_shift})
    for index in temp_shift.index:
        temp.loc[index,'adj_pct_change']=temp_shift.loc[index,'adj_pct_change']


temp.to_csv('../RawData/all_raw_data.csv',encoding='gbk')



