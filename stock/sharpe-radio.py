#coding:utf-8
#夏普比率

import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from datetime import timedelta

#dataframe相关api
#print(df)
#print(df['open'].std())#标准差
#print(len(df))#行数
#print(df.columns.size)#列数
#print(df.columns)#列索引名称
#print(df.index)#行索引名称
#print(df.loc[[df.index[0]],['close']])#第一行列为close

#计算夏普比率
def calcSharpeRadio(df):
	lineNum = len(df)
	std = df['close'].std()
	startOpen = df.loc[[df.index[lineNum-1]],['open']].values[0][0]
	endClose = df.loc[[df.index[0]],['close']].values[0][0]
	radio = (endClose-startOpen)/startOpen/std
	return radio

#根据时间以及夏普比率筛选股票
def sortStocksByRadio(datetime,stocks):
	stocks['radio'] = None;#增加一列

	#上一周第一天和最后一天日期
	lastWeekStart = (now - timedelta(days=now.weekday()+7)).strftime('%Y-%m-%d')
	lastWeekEnd = (now - timedelta(days=now.weekday()+1)).strftime('%Y-%m-%d')
	#print(lastWeekStart);
	#print(lastWeekEnd);

	stocksNum = len(stocks)
	for i in range(stocksNum):
		code = stocks.loc[[stocks.index[i]],['code']].values[0][0]
		df = ts.get_hist_data(code,lastWeekStart,lastWeekEnd)
		radio = calcSharpeRadio(df)
		print('---')
		print(code)
		print(radio)
		stocks.loc[[stocks.index[i]],['radio']] = radio

	sortedStocks = stocks.sort_values(by='radio')

	return sortedStocks

#当前时间
now = datetime.datetime.now()

#获取上证50成份股信息
stocks = ts.get_sz50s()

sortedStocks = sortStocksByRadio(now,stocks)

print(sortedStocks)
