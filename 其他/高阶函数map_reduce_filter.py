'''
map函数

描述：接收两个参数，一个是函数，一个是序列，map将传入的函数依次作用到序列的每个元素。如果传入了多个iterable参数，function 必须接受相同个数的实参并被应用于从所有可迭代对象中并行获取的项。

语法：map(function, iterable, ...)
返回map类型对象
'''
from functools import reduce

'------传入一个序列------------'
mapres=map(lambda x:x*x,[1,2,3,4])
print(type(mapres))
for i in mapres:
    print(i)

'------传入多个个序列------------'
maopres1=map(lambda x,y:x+y,[1,2,3,4],[8,7,6,5])
print(list(maopres1))

'------------------------------reduce-------------------------------------------------'
'''reduce的主要目的是将一个二元操作函数（接受两个参数）应用于序列的元素，以将序列归约为单一的值。
result = reduce(function, sequence[, initial])
function：要应用于序列的二元操作函数。
sequence：要归约的序列，可以是列表、元组等。
initial（可选）：初始值，如果指定，它将成为归约的初始累积值。
'''
#传入初始值
set_a={1,2,3,4,5}
reduce_res0=reduce(lambda x,y:x+y,set_a,10)
print(reduce_res0)

#不传初始值
list_b=[10,22,33,101,3873]

max_value=reduce(lambda x,y:x if x>y else y,list_b)
print(max_value)

'''------------------------------filter-----------------------------------------'''
'''
filter()函数的基本用法
filter()函数的基本语法是：filter(function, iterable)。

function：这是一个返回值为布尔值（True或False）的函数，用于测试可迭代对象的每个元素。
iterable：这是一个可迭代对象，如列表、元组或字符串等。
'''

list_c=[100,200,300,400,500,600]

filter_res=filter(lambda x:  200<=x<500,list_c)

print(list(filter_res))
