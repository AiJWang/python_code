#进制转换
a=18
#转化成2进制
print(bin(a))
#转成8进制
print(oct(a))
#转成16进制
print(hex(a))

#其他进制转10进制
b=0b1001101
print(int(b))

'''
format   ord  chr
'''
print(format(a,'b'))  #转成2进制  b：二进制    o：8进制  x：16进制

print(format(a,'08x')) #16进制 8位，补齐，向前

b='中'  #python的内存使用的编码是unicode

print(ord(b))  #ord 查看对应字符在unicode 中码位
print(chr(12))  #chr与其相反，输入对应码位，展示对应字符
'''
all any  
enumerate 拿到索引和元素

hash：获取hash值
id：获取参数的内存地址 
'''

lis=['张无忌','','赵敏']
print(all(lis))   #列表中所有元素进行与操作
print(any(lis))   #列表中所有元素进行或操作

for index,val in enumerate(lis):
    print(index,val)

print(hash(b))

print(id(b))