get_data.py 是对所有的取数据函数的封装，目前是按照中证500成分股取数据。

adj_data.py 取数据，整理，增加10日涨跌幅，得到最原始的表格。

cal_factors.py 读取adj_data所取得的数据，是因子测试的脚本，已完成因子：BTOP（去极值，标准化，市值行业中性）

