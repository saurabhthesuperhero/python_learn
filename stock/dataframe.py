#coding:utf-8

import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt

df = ts.get_hist_data('sz50')

df.to_csv('./sz50.csv')#保存为csv文件

print(df[0:10])#序号

print(df.ix['2018-10-16':'2018-09-20']);#时间段，需要注意顺序，并不是时间早的在前边

print(df['close'].max())#最大值

print(df['open'].mean())#平均值

print(df[['open','close']])#取多列

#绘图
#df[['low','high']].plot()
#plt.show()

#创建空的dataframe并以date_range中的时间序列为索引
startDate = '2018-09-01'
endDate = '2018-10-16'
dates = pd.date_range(startDate,endDate)
df1 = pd.DataFrame(index=dates)

#整合多个数据
df2 = ts.get_hist_data('600036')#招商银行
df2.to_csv('./600036.csv')
df3 = ts.get_hist_data('000001')#平安银行
df3.to_csv('./000001.csv')
df1 = df1.join(df2['close'])
df1.rename(columns={'close':'600036'}, inplace = True)#重命名列
df1 = df1.join(df3['close'])
df1.rename(columns={'close':'000001'}, inplace = True)

print(df1)
df1.plot()
plt.show()


