'''
此时相当于形成了一个闭包
闭包作用：
    1. 可以让变量常驻内存
    2. 可以避免全局变量被修改
闭包实际上是内层函数对外层函数局部变量的使用，此时内层函数被称为闭包函数
'''

def func():
    a=10
    def inner():
        nonlocal a
        a+=10
        return a
    return inner

c=func()
#因为func返回的是一个函数，所以c可能在任意时间执行，所以a会一直在内存中存在
d=c()
print(d)