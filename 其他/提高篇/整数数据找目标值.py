
'''
给定一个整数数组，和一个目标target值，找出数组中两数之和等于target，返回下标
'''
def get_taget_target(list1,target):
    ss=dict()
    for i in range(len(list1)):
        res=list1[i]
        if num:=ss.get(target-res):
            return i,num
        else:
            ss[res]=i
    return None

def get_ta(lists,tar):
    ss=dict()
    for i in range(len(lists)):
        if num:=ss.get(tar-lists[i]):
            return i,num
        else:
            ss[lists[i]]=i
list1=[1,4,6,8,23]
res=get_ta(list1,27)
print(res)


