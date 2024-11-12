'''
给你一个含 n 个整数的数组 nums ，其中 nums[i] 在区间 [1, n] 内。请你找出所有在 [1, n] 范围内但没有出现在 nums 中的数字，并以数组的形式返回结果。
'''

def getN(nums):
    n=len(nums)
    res=[]
    for i in nums:
        x=(i-1)%n
        nums[x]+=n
    for i in range(n):
        if nums[i]<=n:
            res.append(i+1)
    return res

nums=[1,2,2,4]

print(getN(nums))