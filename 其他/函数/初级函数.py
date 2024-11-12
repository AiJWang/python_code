#定义一个函数，实现计算功能，+ — * /

def acc(a,cha,b):
    if cha=='+':
        print(a+b)
    if cha=='-':
        print(a-b)
    if cha=='*':
        print(a*b)
    if cha=='/':
        print(a/b)

'''
实参传递有很多种形式
    1. 位置参数，跟java一样
    2. 关键字参数
    3. 混合参数，位置参数必须放在前面，关键字参数放在后面
形参也有很多种方式：
    1. 位置参数：就是普通的
    2. 默认值参数：
    3. 动态参数：
        3.1 *args：接受所有位置参数的动态传参,所有参数被放在元组里
        3.2 **kwargs: 接受所有关键字传参，所有元素放在字典里
    形参定义时的参数顺序： 位置参数>*args>默认值>**kwargs
'''

#默认值参数
def defaultP(name,age,gender='男'):
    print(name,age,gender)

#动态传参1
def eatfood(*food):
    print(food)

#混合参数：
def hunhecanshu(a,b,*args,c="东方败",**kwargs):
    print(a,b,args,c,kwargs)

if __name__=='__main__':
    # 传参方式1
    acc(2,'*',3)
    #传参方式2 关键字参数
    acc(b=9,a=8,cha='-')
    #传参方式3 混合方式
    acc(13,"/",b=10)
    print('-------------------')
    #默认值参数
    defaultP('张无忌',18)
    defaultP('赵敏',18,'女')

    #动态参数1
    eatfood('dumplings','noodles')

    #混合参数
    hunhecanshu(1,2,'日出东方','唯我不败',c='东方不败',wugong='葵花宝典')
    hunhecanshu(1, 2, '日出东方', '唯我不败', wugong='葵花宝典')