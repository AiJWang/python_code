class C:

    def getsss(self,kwags):
        print('sss')
        print(kwags)

    def getA(self,*args,**kwargs):
        print(args)
        print(kwargs)
        print(type(args))
        print(type(kwargs))
if __name__=='__main__':
    C().getsss({'ss':12})
    C().getA(12,13,14,15,16,name='getA',age=23,family=['22','33'])