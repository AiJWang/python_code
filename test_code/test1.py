#水仙花数：三位数，各位数字立方和等于该数字本身
def judge_shuixianhua_num(num,judge=False):
    if judge:
        if num not in range(100,1000):
            return False
        gewei=num%10
        shiwei=(num//10)%10
        baiwei=num%100
        return gewei**3+shiwei**3+baiwei**3==num
    else:
        for i  in range(152,1000):
            gewei=i%10
            shiwei=(i//10)%10
            baiwei=i//100
            if gewei**3+shiwei**3+baiwei**3==i:
                print(f'水仙花数字：{i}')

#落地反弹问题，一个球从100米高落下，每次落地后反弹到原来高度一半，在落地，求它第10次落地时走了多少米
def fantan(times,high=100):
    n=0
    total=0
    while n<times:
        if n==0:
            total+=high
            high/=2
        else:
            total+=2*high
            high/=2
        n+=1
    return total

#猴子吃桃问题，猴子第一天摘了n个桃子，第一天吃了其中一半 +1个，第二天吃了昨天剩的一半加一个，到第十天，还剩1个了，求n
def get_peach():
    n,total=1,0
    for i in range(9):
        total=(n+1)*2
        n=total
    return total
#判断一会字符串是不是回文字符串
def judge_huiwen(a):
    return a[::-1]==a
if __name__ == '__main__':
    print(judge_huiwen('abccerba'))
