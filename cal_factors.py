import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn import preprocessing

raw_data=pd.read_csv('../RawData/all_raw_data.csv',encoding='gbk')
date=list(raw_data.groupby(by=['trade_date'],as_index=False).size().index)

industry_dummies=pd.get_dummies(raw_data['Industry'])


raw_data['lnCap']=np.log(raw_data['total_mv'])


##########################以下是准备
raw_data['btop']=1/raw_data['pb']

X=pd.concat([raw_data['lnCap'],industry_dummies],axis=1)
Y=raw_data['btop']

Y=pd.concat([Y,X],axis=1)
Y=pd.concat([raw_data['trade_date'],raw_data['adj_pct_change'],Y],axis=1)

########################### 此时Y的结构是：日期，未来变化率，因子，中性化项目


predict_window=10   #和adj_data中一致
k=2                 #过去几日数据的时间窗
btop_ic = pd.DataFrame([])

#raw_industry=pd.get_dummies(raw_data)

for i in range(k-1,len(date)-predict_window):
    temp = pd.DataFrame([])
    print('solving date '+str(date[i]))
    for j in range(k):
        temp=temp.append(Y[Y['trade_date']==date[i-j]])

    temp = temp.reset_index()
    temp.drop(columns=['index'], inplace=True)

    nanblank = np.where(np.isnan(temp['btop']))
    nanblank = list(nanblank[0])
    temp = temp.drop(nanblank)

    temp['btop'] = preprocessing.scale(temp['btop'])
    temp['lnCap'] = preprocessing.scale(temp['lnCap'])
    result = sm.OLS(temp['btop'], temp.iloc[:, range(4, 32)]).fit()
    temp['btop'] = result.resid

    btop_ic=btop_ic.append([temp['btop'].corr(temp['adj_pct_change'])])

btop_ic=btop_ic.reset_index()
btop_ic.drop(columns=['index'],inplace=True)
date_slice=pd.DataFrame(date[k-1:len(date)-predict_window])


btop_ic=pd.DataFrame({'trade_date':date_slice[0],'IC':btop_ic[0]})

btop_ic.to_csv('../RawData/BTOP_IC.csv')


