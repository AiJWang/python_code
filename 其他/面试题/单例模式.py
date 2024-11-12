
def danli(cls):
    s=dict()
    def inner(*args,**kwargs):
        if len(s)<0:
            s[cls]=cls(*args,**kwargs)
        return s[cls]
    return inner

@danli
class Person():
    pass