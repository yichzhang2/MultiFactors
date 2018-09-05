import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression

raw_data=pd.read_csv('../RawData/all_raw_data.csv',encoding='gbk')
date=list(raw_data.groupby(by=['trade_date'],as_index=False).size().index)

industry_dummies=pd.get_dummies(raw_data['Industry'])


raw_data['lnCap']=np.log(raw_data['total_mv'])


##########################以下是准备
raw_data['btop']=1/raw_data['pb']

X=pd.concat([raw_data['lnCap'],industry_dummies],axis=1)
Y=raw_data['btop']

Y=pd.concat([Y,X],axis=1)
Y=pd.concat([raw_data['trade_date'],raw_data['pct_chg_shift'],Y],axis=1)

Y.drop(['食品饮料'],axis=1, inplace=True)

########################### 此时Y的结构是：日期，未来变化率，因子，中性化项目



def winsorize(factor, std=3, have_negative = True):
    '''
    去极值函数
    factor:以股票code为index，因子值为value的Series
    std为几倍的标准差，have_negative 为布尔值，是否包括负值
    输出Series
    '''
    r=factor.copy()
    #取极值
    edge_up = r.mean()+std*r.std()
    edge_low = r.mean()-std*r.std()
    r[r>edge_up] = edge_up
    r[r<edge_low] = edge_low
    return r



predict_window=10   #和adj_data中一致
k=1                 #过去几日数据的时间窗
btop_ic = pd.DataFrame([])
btop_factor_premium = pd.DataFrame([])

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

    temp['btop']=winsorize(temp['btop'])
    temp['lnCap'] = winsorize(temp['lnCap'])

    temp['btop'] = preprocessing.scale(temp['btop'])
    temp['lnCap'] = preprocessing.scale(temp['lnCap'])
    result = sm.OLS(temp['btop'], temp.iloc[:, range(4, 31)]).fit()
    temp['btop'] = result.resid

    btop_ic=btop_ic.append([temp['btop'].corr(temp['pct_chg_shift'],method='spearman')])
    linreg= sm.OLS(temp['btop'], temp['pct_chg_shift']).fit()

    btop_factor_premium=btop_factor_premium.append([linreg.params[0]])

btop_ic=btop_ic.reset_index()
btop_ic.drop(columns=['index'],inplace=True)

btop_factor_premium=btop_factor_premium.reset_index()
btop_factor_premium.drop(columns=['index'],inplace=True)

date_slice=pd.DataFrame(date[k-1:len(date)-predict_window])

btop=pd.DataFrame({'trade_date':date_slice[0],'IC':btop_ic[0],'Factor_Premium':btop_factor_premium[0]})

print('positive percentage: '+str(btop[btop['IC']>0].count().IC/(len(date)-predict_window-k+1)))     #仅仅k=1时成立
print('average IC: '+ str(btop['IC'].mean()))   #仅仅k=1时成立

btop.to_csv('../RawData/BTOP_IC.csv')


