#元组 不可变
ta=(1,2,'we','are',['fa','ily'])
print(ta)
#判断元素在元组中位置
print(ta.index('we'))
#获取对应位置元素
print(ta[1])
#查询元素个数
print(ta.count('we'))
ta[4].append('look')
print(ta[4])
#判断元素是否在元组中
print (['fa', 'ily', 'look'] in ta)


print('--------------------------------liebiao')

#liebiao  有序，可重复

list1=list()

list1.append('远看')
print(list1)
list1.extend(['山','色'])
print(list1)
list1.insert(2,'有')
print(list1)

list1.pop()

print(list1)

list1.pop(0)
print(list1)

list1.remove('山')
print(list1)

list2=['ac','a','ab','dc']
#排序
list2.sort()
print(list2)

list2.sort(reverse=True)
print(list2)

print('-----------------------')
#集合  无序，不重复
set1=set()
set1.add('i')
set1.add('love')
set1.update({'i','like','meet'})
print(set1)

set2={'i','love','china'}
#交集
print(set1&set2)
#并集
print(set1|set2)
#差集
print(set1-set2)

print('---------------------------------------')

#zidian
dict1=dict()
dict1['tian']='di'
print(dict1)
dict1.update({'rain':'wind','mainland':'sky'})
print(dict1)


#查所有key
for key in dict1:
    print(key)
print('---------------')
#返回所有key
print(list(dict1.keys()))
#返回所有value
print(dict1.values())
#遍历所有元素
for item in dict1.items():
    print(item)
print('-----------------')
#返回所有key value
for key,val in dict1.items():
    print(key,val)

print('-----------')
#解包
a,b,c=[1,2,3]
print(a)
print(b)
print(c)

print(dict1['mainland'])
#字典里不存在key是返回none
print(dict1.get('hahaha'))