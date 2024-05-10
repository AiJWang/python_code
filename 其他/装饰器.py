import functools


def add_list(func):
    @functools.wraps(func)
    def inner(args,kwargs):
        print('执行装饰器内部函数')
        res=func(args,kwargs)
        return res*2
    return inner

@add_list
def add_num(a,b):
    '''add nnnnnn'''
    print(a+b)
    print(add_num.__name__)
    print(add_num.__doc__)
    return a+b

if __name__ == '__main__':
    res=add_num(1,2)
    print(res)