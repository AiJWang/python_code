a=10

def geta():
    a=20   #此时只是相当于声明了一个局部变量a，不能改变全局变量a

geta()
print(a)

def changea():
    global a   #相当与声明此a就是全局变量的a
    a=20

changea()
print(a)

def changeb():
    b='哈哈'
    def chass():
        nonlocal b    #相当与声明此b就是外部的局部变量
        b='笑书神侠倚碧鸳'
    chass()
    print(b)


changeb()