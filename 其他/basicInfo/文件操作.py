

import os
'''
1. 找到文件，打开

open(文件路径，mode="", encoding="")
mode：r 读
     w 写
     a  追加写入
     读写非文本时需要加上b
     rb
     wb
with: 上下文，不用自己close

'''

#在相同文件夹下，直接打开


open('国产自拍.txt')

#在不同文件夹下，去对应路径下打开
open('../葫芦娃.txt')
open('../source/神雕侠侣.txt')

f=open('国产自拍.txt',mode='r',encoding='utf-8')
#一次性全部读取
content=f.read()
print(content)
f.close()
f=open('国产自拍.txt',mode='r',encoding='utf-8')
#一次读取所有，放在列表里
content=f.readlines()
print(content)
f.close()
f=open('国产自拍.txt',mode='r',encoding='utf-8')
#每次读一行
content=f.readline()
f.close()
print(content.strip())

#最重要的
f=open('国产自拍.txt',mode='r',encoding='utf-8')
for line in f:  #相当于每次读一行
    print(line.strip())
f.close()

print('----------------------')
# 写操作 mode=w，此模式下，若文件不存在，则创建文件，若存在，则被清空
f1=open('咏鹅.txt',mode='w',encoding='utf-8')
lines=['  唐 骆宾王','鹅，鹅，鹅','曲项向天歌','白毛浮绿水','红掌拨清波']
for line in lines:
    f1.write(line+'\n')
f1.close()

f2=open('咏鹅.txt',mode='a',encoding='utf-8')
f2.write("hahaha")
f2.close()

print('--------------')
with open('国产自拍.txt',mode='r',encoding='utf-8') as f:
    for line in f:
        print(line.strip())

#读写非文本数据 照片
file ='C:\\Users\\24482\\Desktop\\刘亦菲\\刘亦菲.webp'
with open(file,mode='rb') as f:
    for line in f:
        print(line)
#文件复制：将桌面上刘亦菲照片复制到当前路径
#必须写  \  代表下面一行和当前行是一行代码
with open(file,mode='rb') as f, \
    open('刘亦菲c.jpeg',mode='wb') as f1:
    for line in f:
        f1.write(line)

#修改文件，将文件中姓周的改成姓王的，思路为先循环读源文件数据，处理数据，写入新文件，将 源文件删除，将新文件重命名为源文件

with open('咏鹅.txt',mode='r',encoding='utf-8') as f, \
     open('咏鹅1.txt', mode='w', encoding='utf-8') as f1:
    for line in f:
        line =line.strip();
        if line.startswith('白'):

            line='红'+line[1:]
        elif line.startswith('红'):
            line = '白' + line[1:]
        line=line+'\n'
        f1.write(line)

os.remove('咏鹅.txt')
os.rename('咏鹅1.txt','咏鹅.txt')