#coding:utf-8

import numpy as np

#创建ndarray

print(np.array([(0,1,2,3),(4,5,6,7)]))

print(np.empty((2,4)))

print(np.ones((2,4)))

print(np.ones((2,4),dtype=np.int_))

print(np.random.random((2,4)))

print(np.random.normal(50,10,size=(2,4)))

print(np.random.randint(0,10,size=(2,4)))

#属性

na = np.random.randint(0,10,size=(2,4))

print(na.shape)

print(na.size)

print(na.dtype)

#方法

print(na.sum())