'''
:return 可以多个返回值，多个返回值以元组方式返回
'''

def sumin(*args):
    sum=0
    for i in args:
        sum+=i
    return sum

def reman():
    return 1,2,3

if __name__=='__main__':
    aa=sumin(2,3,4)
    print(aa)
    ma=reman()
    print(ma)