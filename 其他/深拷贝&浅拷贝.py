
'''复制，未进行考培，list1和list2任意修改，都会导致另外一个也跟着修改'''
from copy import deepcopy

list1=[1,2,3,4]
list2=list1

'''浅拷贝，只拷贝一层'''
list1=[1,2,3,[4,5]]
list2=list1.copy()
list1[0]=10 #此时list2不变
list1[-1][-1]=33 #此时list2也变了
print(list1,list2)

'''深拷贝，所有层数数据都拷贝了'''
list3=deepcopy(list1)
list1[-1][-1]=30
print(list1,list3)

