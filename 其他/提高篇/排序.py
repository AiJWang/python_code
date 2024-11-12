'''冒泡排序'''
def maopao(s):
    le=len(s)
    for i in range(le):
        for j in range(le-1-i):
            if s[j]>s[j+1]:
                s[j],s[j+1]=s[j+1],s[j]

'''选择排序'''
def xuanze(s):
    le=len(s)
    for i in range(le):
        a=i
        for j in range(i+1,le):
            if s[a]>s[j]:
                a=j
        if a!=i:
            s[a],s[i]=s[i],s[a]


s=[6,4,9,1,0,3,10,2,5]

xuanze(s)
print(s)


