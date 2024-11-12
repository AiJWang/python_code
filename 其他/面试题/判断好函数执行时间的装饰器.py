'''函数执行时间的装饰器'''
import datetime
import time



def outer(fn):
    def inner(*args,**kwargs):
        start=datetime.datetime.now()
        res=fn(*args,**kwargs)
        end=datetime.datetime.now()
        print(end-start)
        return res
    return inner

@outer
def saybye():
    time.sleep(3)


saybye()