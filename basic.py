#coding:utf-8

'''
SyntaxError: Non-ASCII character
python中默认编码格式是ASCII，所以在没有修改编码格式时文件中不能出现中文，那怕是注释！
解决办法是加上上述声明。
'''

'''
python基础语法学习
python基础语法学习
'''

# 加载随机模块
from random import randint

i = randint(0,100)

print(i)

# for循环

for i in range(0,5,1):
	print(i)