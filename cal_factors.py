import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

raw_data=pd.read_csv('../RawData/all_raw_data.csv',encoding='gbk')
date=list(raw_data.groupby(by=['trade_date'],as_index=False).size().index)

k=5 #过去5天的时间窗
pb_ic = pd.DataFrame([])


for i in range(len(date)-k+1): #逻辑是对的,末尾出现NAN是因为adj_pct_change的时间窗在adj_data里有设置时间窗
    temp = pd.DataFrame([])
    print('solving date '+str(date[i]))
    for j in range(k):
        temp=temp.append(raw_data[raw_data['trade_date']==date[i+j]])
    pb_ic=pb_ic.append([temp['pb'].corr(temp['adj_pct_change'])])

pb_ic=pb_ic.reset_index()
pb_ic.drop(columns=['index'],inplace=True)
pb_ic=pb_ic.append(pd.DataFrame(np.zeros((k-1,1))))
pb_ic_shift=pb_ic.shift(k-1)
pb_ic_shift=pb_ic_shift.reset_index()
pb_ic_shift.drop(columns=['index'],inplace=True)

pb_ic_shift = pd.DataFrame({'trade_date':date,'ic': pb_ic_shift[0]})
temp=pb_ic_shift #备份
pb_ic_shift.trade_date=pd.to_datetime(pb_ic_shift.trade_date,format='%Y%m%d')

pb_ic_shift.to_csv('../RawData/FactorIC.csv')



plt.figure()
plt.plot(pb_ic['trade_date'],pb_ic_shift['ic'])
plt.show()