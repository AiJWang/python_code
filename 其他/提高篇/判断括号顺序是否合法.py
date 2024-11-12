'''
 * 给出一个仅包含字符'(',')','{','}','['和']',的字符串，判断给出的字符串是否是合法的括号序列
 * 括号必须以正确的顺序关闭，"()"和"()[]{}"都是合法的括号序列，但"(]"和"([)]"不合法。
 * *'''



def judge_kuohao(s):
    lista=list()
    for i in range(len(s)):
        if s[i] in ['(','[','{']:
            lista.append(s[i])
        else:
            if len(lista)>0:
                b=lista.pop()
                if s[i]==')':
                    if b!='(':
                        return False
                elif s[i]==']':
                    if b!='[':
                        return False
                else:
                    if b!='{':
                        return False
            else:
                return False
    return len(lista)==0

s='['
print(judge_kuohao(s))