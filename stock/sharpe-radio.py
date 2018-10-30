#coding:utf-8
#夏普比率

import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from datetime import timedelta

def calcSharpeRadio(df):
	lineNum = len(df)
	std = df['close'].std()
	startClose = df.loc[[df.index[lineNum-1]],['close']].values[0][0]
	endClose = df.loc[[df.index[0]],['close']].values[0][0]
	radio = (endClose-startClose)/startClose/std
	return radio

#当前时间
now = datetime.datetime.now()

#上一周第一天和最后一天日期
lastWeekStart = (now - timedelta(days=now.weekday()+7)).strftime('%Y-%m-%d')
lastWeekEnd = (now - timedelta(days=now.weekday()+1)).strftime('%Y-%m-%d')
#print(lastWeekStart);
#print(lastWeekEnd);

#测试夏普比率
df = ts.get_hist_data('000001',lastWeekStart,lastWeekEnd)
#print(df)
#print(df['open'].std())#标准差
#print(len(df))#行数
#print(df.columns.size)#列数
#print(df.columns)#列索引名称
#print(df.index)#行索引名称
#print(df.loc[[df.index[0]],['close']])#第一行列为close
print(calcSharpeRadio(df))

#计算上证50成份股夏普比率
stocks = ts.get_sz50s()
stocks['radio'] = None;#增加一列
stocksNum = len(stocks)
for i in range(stocksNum):
	code = stocks.loc[[stocks.index[i]],['code']].values[0][0]
	df = ts.get_hist_data(code,lastWeekStart,lastWeekEnd)
	radio = calcSharpeRadio(df)
	stocks.loc[[stocks.index[i]],['radio']] = radio

sortedStocks = stocks.sort_values(by='radio')
print(sortedStocks)
