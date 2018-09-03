import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import statsmodels.api as sm

from datetime import datetime
#import matplotlib.pyplot as plt

raw_data=pd.read_csv('../RawData/all_raw_data.csv',encoding='gbk')
date=list(raw_data.groupby(by=['trade_date'],as_index=False).size().index)

industry_dummies=pd.get_dummies(raw_data['Industry'])
#raw_data= pd.concat([raw_data,industry_dummies],axis=1)

raw_data['btop']=1/raw_data['pb']

raw_data['lnCap']=np.log(raw_data['total_mv'])
X=pd.concat([raw_data['lnCap'],industry_dummies],axis=1)
Y=raw_data['btop']

result = sm.OLS(Y.head(50000),X.head(50000)).fit()

predict_window=10
k=2 #过去5天的时间窗
pb_ic = pd.DataFrame([])

#raw_industry=pd.get_dummies(raw_data)

for i in range(k-1,len(date)-predict_window):
    temp = pd.DataFrame([])
    print('solving date '+str(date[i]))
    for j in range(k):
        temp=temp.append(raw_data[raw_data['trade_date']==date[i-j]])

    #此处此处加

    pb_ic=pb_ic.append([temp['pb'].corr(temp['pct_chg_shift'])])

pb_ic=pb_ic.reset_index()
pb_ic.drop(columns=['index'],inplace=True)
date_slice=pd.DataFrame(date[k-1:len(date)-predict_window])


pb_ic=pd.DataFrame({'trade_date':date_slice[0],'IC':pb_ic[0]})

pb_ic.to_csv('../RawData/FactorIC.csv')



plt.figure()
plt.plot(pb_ic['trade_date'],pb_ic_shift['ic'])
plt.show()