'''
假设有一个n阶的楼梯，你每次只能走1阶或者2阶，请问有多少种上楼方法
'''
resdisss=dict()

def palouti(n):
    if n==1:
        return 1
    if n==2:
        return 2

    return palouti(n-1)+palouti(n-2)


if __name__ == '__main__':
    res=palouti(3)
    print(res)