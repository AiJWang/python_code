
'''
在Python编程中，生成器（Generator）是一个强大而又灵活的工具，它允许您在需要的时候生成一系列的值，而不必一次性将它们全部存储在内存中
生成器最常见的形式是使用函数定义，其中包含一个或多个yield语句。当函数执行到yield语句时，
它会产生一个值并暂停执行，将值返回给调用者。当生成器再次被调用时，它会从上次暂停的位置继续执行，直到再次遇到yield语句。

'''
def add_num(*args):
    for i in args:
        yield i*i


res=add_num(1,2,3)
print(next(res))
print('-------')
for i in res:
    print(i)

