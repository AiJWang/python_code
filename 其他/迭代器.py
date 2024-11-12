'''
迭代器有点
‌节省内存‌：迭代器一次只返回一个元素，不需要一次性将整个集合加载到内存中，这对于处理大型数据集合非常有用，可以显著减少内存的使用。
‌惰性计算‌：迭代器在需要时才计算下一个元素，而不是一次性计算所有元素，这种方式可以提高处理大量数据的效率。
‌可逆迭代‌：迭代器可以反向遍历集合，而不需要额外的复制和存储，提供了更大的灵活性。
‌支持并行处理‌：迭代器可以同时遍历多个集合，实现并行处理，进一步提高处理速度和效率。
‌遍历集合‌：迭代器可以用于遍历各种Python内置的数据类型，如列表、元组、字典和集合等。
'''

'''
可迭代对象：实现 __iter__ 方法,并且返回值是迭代器对象
'''
class kediedai:
    def __init__(self):
        self.a=[1,2,3,4]
    def __iter__(self):
        return self.a

'''
迭代器：
    1. 类中定义了 __iter__  和 __next__ 方法
    2. __iter__ 方法返回对象本身，即self
    3. __next__ 方法返回下一个数据，如果没有数据了，抛出 stopIteration 异常
'''
class newRange(object):
    def __init__(self,it):
        self.counter=-1
        self.it=it
    def __iter__(self):
        return self
    def __next__(self):
        self.counter+=1
        if self.counter==self.it:
            raise StopIteration()
        return self.counter

class Xrange:
    def __init__(self,num):
        self.a=num
    def __iter__(self):
        return newRange(self.a)

if __name__ == '__main__':
    s=Xrange(5)
    # print(next(s))
    # print('-'*10)
    for i in s:
        print(i)