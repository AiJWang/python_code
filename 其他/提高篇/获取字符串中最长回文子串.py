

def gethuiwen(s):
    les=0
    strs=''
    le=len(s)
    for i in range(len(s)):
        l,r=i,i
        while (l>=0 and r<le and s[l]==s[r]):
            if (r-l+1)>les:
                les=r-l+1
                strs=s[l:r+1]
            l-=1
            r+=1
        l,r=i,i+1
        while l>=0 and r<len(s) and s[l]==s[r]:
            if (r-l+1)>les:
                les=r-l+1
                strs=s[l:r+1]
            l-=1
            r+=1
    return les,strs


str='dcbabcc'
print(gethuiwen(str))
print(-1>=0&1<len(str)&str[-1]==str[1])