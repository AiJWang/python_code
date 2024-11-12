
'''

函数嵌套

1. 函数可以作为返回值返回
2. 函数可以作为参数传递

函数名实际就是一个变量名  不要加（）
'''
#函数内还可定义函数
def fun1():
    b=20
    def fun2():
        print(b)
        pass

#返回值是一个函数，把函数当成变量返回了
def func1():
    def inner():
        print('this is inner')
    return inner       #将函数当成变量返回了，但是不能加括号

#代理模式    函数当成参数进行传递
def target():
    print('this is target')

def soul(a):
    a()
    print('this is soul')


if __name__=='__main__':
    ins=func1()
    print(ins)
    print(ins())
    print(soul(target))