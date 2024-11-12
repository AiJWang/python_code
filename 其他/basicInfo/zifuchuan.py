#1. 字符串格式化 %s 字符串占位符  %d 数字占位符
name=input('请输入你的名字：')
age=int(input('请输入你的年龄：'))
address=input('请输入你的住址：')

words='我叫%s，我今年%d岁了，我住在%s' % (name,age,address)
print(words)

#方式2
words2='我叫{}，我今年{}岁了，我住在{}'.format(name,age,address)
print(words2)

#方式3
words3=f'我叫{name},今年{age}岁，住在{address}'
print(words3)

#索引 和切片

s="飞来山上千寻塔"
print(s[0])  #正数第一个位置
print(s[-1]) #倒数第一个位置

#切片
print(s[1:3]) #左闭右开

print(s[:3]) #从头切到3
print(s[2:]) #从2切到尾

print(s[-3:-1]) #从左往右切

print(s[::2]) #2是切片的步长

print(s[::-2]) #2是切片的步长。-表示从右往左切

#字符串常规操作

newword='i have a dream'

print(newword.title()) #每个单词首字母大写
print(newword.lower()) #每个单词小写
print(newword.upper()) #所有单词大写
print(newword.capitalize()) #首字母大写