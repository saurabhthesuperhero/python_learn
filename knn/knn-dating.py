#coding:utf-8

from numpy import *
import matplotlib.pyplot as plt
import operator

def file2matrix(filename):
	fr = open(filename)#打开文件
	lines = fr.readlines()#逐行读取

	length = len(lines)#行数
	mat = zeros((length,3))#空矩阵
	labels = []

	index = 0
	for line in lines:
		line = line.strip()#去掉首尾的空白或者换行符
		array = line.split('\t')#用制表符拆分字符串
		mat[index,:] = array[0:3]#矩阵赋值，取前3位
		labels.append(int(array[-1]))#取最后一位
		index += 1

	return mat,labels

#准备数据

'''
各数据项意义如下：
每年获得的飞行常客里程数、玩视频游戏所耗时间百分比、每周消费的冰淇淋公升数、兴趣指数；
兴趣指数：3表示极具魅力、2表示魅力一般、1表示不喜欢。
'''
mat,labels = file2matrix('./dating-set.txt')



#归一化数值

'''
因为各项数据的单位不一致，导致对距离的计算影响因子也不一致；
也就是说每年获得飞行常客里程数对于计算结果的影响将远远大于其它两个特征；
这和我们假定三个特征值是等权重的冲突，此时需要我们进行归一化处理，让三个特征值均处于0-1区间；
公式如下：
newValue = (oldValue-min)/(max-min)
'''

def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals, (m,1))
    normDataSet = normDataSet/tile(ranges, (m,1)) 
    return normDataSet, ranges, minVals

normDataSet,ranges,minVals = autoNorm(mat)



#分析数据
#fig = plt.figure()

#a1 = fig.add_subplot(121)#子图
#a1.scatter(normDataSet[:,0],normDataSet[:,1],15.0*array(labels),15.0*array(labels))

#a2 = fig.add_subplot(122)
#a2.scatter(normDataSet[:,1],normDataSet[:,2],15.0*array(labels),15.0*array(labels))

#plt.show()



# k近邻算法实现
def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX, (dataSetSize,1)) - dataSet
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5
    sortedDistIndicies = distances.argsort()     
    classCount={}          
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]



# 测试
def datingTest():
    hoRatio = 0.50#选取百分之十的数据去测试
    datingDataMat,datingLabels = file2matrix('./dating-set.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m*hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i,:],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],3)
        print "the classifier came back with: %d, the real answer is: %d" % (classifierResult, datingLabels[i])
        if (classifierResult != datingLabels[i]): errorCount += 1.0
    print "the total error rate is: %f" % (errorCount/float(numTestVecs))
    print errorCount

datingTest()    