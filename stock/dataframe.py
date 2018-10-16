#coding:utf-8

import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt

df = ts.get_hist_data('sz50')

df.to_csv('./sz50.csv')#保存为csv文件

print(df[0:10])#序号

print(df['close'].max())#最大值

print(df['open'].mean())#平均值

#创建空的dataframe并以date_range中的时间序列为索引
startDate = '2018-01-01'
endDate = '2018-12-31'
dates = pd.date_range(startDate,endDate)
df1 = pd.DataFrame(index=dates)

#绘图
#df1[['low','high']].plot()
#plt.show()