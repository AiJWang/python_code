from 其他.装饰器 import print_dec


class C:
    @print_dec
    def getsss(self,kwags):
        print('sss')
        print(kwags)

    def getA(self,*args,**kwargs):
        print(args)
        print(kwargs)
        print(type(args))
        print(type(kwargs))
if __name__=='__main__':
    c=C()
    print(c)
    c.getsss({'ss':12})
