'''
假设有一个n阶的楼梯，你每次只能走1阶或者2阶，请问有多少种上楼方法
'''
resdisss=dict()

def palouti(n):
    if n<3:
        return n
    if res:=resdisss.get(n,None):
        return res
    else:
        res=palouti(n-1)+palouti(n-2)
        resdisss[n]=res
    return res


def palouti1(n):
    if n<3:
        return n
    n1,n2,res,i=1,2,0,3
    while i<=n:
        res=n1+n2
        n1,n2=n2,res
        i+=1
    return res


if __name__ == '__main__':
    res=palouti(50)
    print(res)
    res1=palouti1(50)
    print(res1)