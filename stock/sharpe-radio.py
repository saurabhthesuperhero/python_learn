#coding:utf-8
#夏普比率

import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from datetime import timedelta

ts.set_token('a2904e605fd3caf157ba1f90d0a0b52f4168ed53db4d8964b99938cf')#设置token
print(ts.__version__)#tushare 版本
tsPro = ts.pro_api()#tushare pro api

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
	radio = 0

	if lineNum>0:
		std = df['close'].std()
		startOpen = df.loc[[df.index[lineNum-1]],['open']].values[0][0]
		endClose = df.loc[[df.index[0]],['close']].values[0][0]
		radio = (endClose-startOpen)/startOpen/std

	return radio

#根据时间以及夏普比率筛选股票
def sortStocksByRadio(datetime,stocks,nums):
	stocks['radio'] = None;#增加一列

	#上一周第一天和最后一天日期
	lastWeekStart = (datetime - timedelta(days=datetime.weekday()+7)).strftime('%Y-%m-%d')
	lastWeekEnd = (datetime - timedelta(days=datetime.weekday()+1)).strftime('%Y-%m-%d')
	#print(lastWeekStart);
	#print(lastWeekEnd);

	stocksNum = len(stocks)
	if nums>stocksNum :
		nums = stocksNum

	for i in range(stocksNum):
		code = stocks.loc[[stocks.index[i]],['code']].values[0][0]
		df = ts.get_hist_data(code,lastWeekStart,lastWeekEnd)
		radio = calcSharpeRadio(df)
		stocks.loc[[stocks.index[i]],['radio']] = radio

	sortedStocks = stocks.sort_values(by='radio')
	#print(sortedStocks)

	codes = []
	for i in range(nums):
		codes.append(sortedStocks.loc[[sortedStocks.index[stocksNum-1-i]],['code']].values[0][0])

	return codes

#计算日期所在周的收益
def calBenifit(datetime,codes,money):

	thisWeekStart = (datetime - timedelta(days=datetime.weekday())).strftime('%Y-%m-%d')
	thisWeekEnd = (datetime + timedelta(days=6-datetime.weekday())).strftime('%Y-%m-%d')

	stocksNum = len(codes)
	itemMoney = money*1.0/stocksNum#暂时均衡投资

	result = 0

	for i in range(stocksNum):
		df = ts.get_hist_data(codes[i],thisWeekStart,thisWeekEnd)
		lineNum = len(df)
		if lineNum>0:
			startOpen = df.loc[[df.index[lineNum-1]],['open']].values[0][0]
			endClose = df.loc[[df.index[0]],['close']].values[0][0]
			benifit = itemMoney*(1+(endClose-startOpen)/startOpen)
			print(codes[i]+' '+repr(benifit))
			result = result + benifit
		else:
			print(codes[i]+' No Data')
			result += itemMoney



	return result


#当前时间
now = datetime.datetime.now()

#获取上证50成份股信息
stocks = ts.get_sz50s()

#筛选股票
codes = sortStocksByRadio(now,stocks,5)

print(calBenifit(now,codes,1))


