import functools



def print_dec(func):
    def inner(*args,**kwargs):
        print('执行内部函数')
        print(args[0])
        print(args[1])
        print('-'*10)
        func(*args,**kwargs)
    return inner

def add_list(func):
    #functools.wraps 的作用就是保持被装饰的函数名及描述，否则就会变成装饰函数的名字
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


def handel_num(type):
    def outer_func(func):
        print('outer_func')
        def inner_func(*args,**kwargs):
            print('inner_func')
            if type=='+':
                res=func(*args,type='+')
            else:
                res=func(*args,type='*')
            return res
        return inner_func
    return outer_func

@handel_num("+")
def num_handel(*args,type='+'):
    if type=='+':
        res=functools.reduce(lambda x,y:x+y,args)
        print(res)
        return res
    else:
        res=functools.reduce(lambda x,y:x*y,args)
        print(res)
        return res




if __name__ == '__main__':
    num_handel(1,2,3,4,type='+')