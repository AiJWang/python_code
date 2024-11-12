'''/**
 * 正整数 n 代表生成括号的对数，请设计一个函数，用于能够生成所有可能的并且 有效的 括号组合。
 * 输入：n = 3
 * 输出：["((()))","(()())","(())()","()(())","()()()"]
 * */'''
# result=[]
# print(type(result))
# def generate_kuohao(l,r,n,result,res):
#     if r>l:
#         return
#     if r==n and l==n:
#         result.append(res)
#     if l<n:
#         generate_kuohao(l+1,r,n,result,res+'(')
#     if r<n:
#         generate_kuohao(l,r+1,n,result,res+')')
#
# generate_kuohao(0,0,3,result,'')
# print(result)
class Solution(object):
    def generateParenthesis(self, n):
        """
        :type n: int
        :rtype: List[str]
        """
        result=[]
        self.generate_kuohao(0, 0, n, result,str())
        return result

    def generate_kuohao(self,l,r,n,result,res):
        if r>l:
            return
        if r==n and l==n:
            result.append(res)
        if l<n:
            self.generate_kuohao(l+1,r,n,result,res+'(')
        if r<n and r<l:
            self.generate_kuohao(l,r+1,n,result,res+')')

if __name__ == '__main__':
    so=Solution()
    res=so.generateParenthesis(3)
    print(res)