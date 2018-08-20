#coding:utf-8

from math import log

'''
海洋生物数据集合
不浮出水面是否可以生存、是否有脚蹼、是否属于鱼类
'''
dataset = [
	[1,1,'yes'],
	[1,1,'yes'],
	[1,0,'no'],
	[0,1,'no'],
	[0,1,'no'],
]

#特征标签
labels = ['no surfacing','flippers']

#计算给定数据集的香农熵
def calcShannonEnt(dataset):
	numEntries = len(dataset)#计算数据集中实例总数
	labelCounts = {}

	for featVec in dataset:
		currentLabel = featVec[-1]
		if currentLabel not in labelCounts.keys():
			#如果当前类别暂时没有被统计则初始化为1
			labelCounts[currentLabel] = 1
		else:
			#否则在以前的统计数据上递增1
			labelCounts[currentLabel] += 1	

	shannonEnt = 0.0#香农熵

	for key in labelCounts:
		prob = float(labelCounts[key])/numEntries
		shannonEnt -= prob * log(prob,2)

	return shannonEnt


#选取特征axis为value的数据
def splitDataSet(dataset,axis,value):
	retDataset = []
	for featVec in dataset:
		#如果当前元素复合
		if featVec[axis] == value:
			reducedFeatVec = featVec[:axis]
			reducedFeatVec.extend(featVec[axis+1:])
			retDataset.append(reducedFeatVec)

	return retDataset

#选取最好的信息划分特征
def chooseBestFeatureToSplit(dataset):
	numFeatures = len(dataset[0])-1#根据第一项样本数据获取特征数
	baseEntropy = calcShannonEnt(dataset)
	bestInfoGain = 0.0
	bestFeature = -1#最好的划分特征序号

	for i in range(numFeatures):
		featList = [example[i] for example in dataset]#获取样本数据中的第i项特征
		uniqueVals = set(featList)
		newEntropy = 0.0

		for value in uniqueVals:
			subDataSet = splitDataSet(dataset,i,value)
			prob = len(subDataSet)/float(len(dataset))
			newEntropy += prob*calcShannonEnt(subDataSet)

		infoGain = baseEntropy - newEntropy#信息增益
		if(infoGain > bestFeature):
			bestInfoGain = infoGain
			bestFeature = i

	return bestFeature			


#测试计算香农熵
#print(calcShannonEnt(dataset))

#测试特征选取
#print(splitDataSet(dataset,0,1))#选取序号为0的特征，值为1的数据项
#print(splitDataSet(dataset,0,0))#选取序号为0的特征，值为0的数据项

print(chooseBestFeatureToSplit(dataset))