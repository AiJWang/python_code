a=" 赵敏，我是   张无忌啊  "
print(a.strip())
print("赵敏" in a)
print(a.strip()[::-1])
print(a.strip()[2:5])
c="12345678"
print(c[-4:-2])

b=["haha","34","23"]
print("-".join(b))

print('--------------------------')
'''---------------------------------列表操作--------------------------------------'''
c=list()
c.append(12)
c.append('你好')
c.append('哈哈')
print(c)
c.insert(0,"guo")
print(c)
c.pop(2)
print(c)
c.extend(["gag","dsds"])
print(c)
c.remove('dsds')
print(c)
c=[12,33,11,66,23]
c.sort()
print(c)
c.sort(reverse=True)
print(c)
'''---------------------------------元祖操作--------------------------------------'''
#元祖 tuple
d=(1,'ew',32,33,33)
print(d[2])
print(d.count(33))
'''---------------------------------set集合操作--------------------------------------'''
#set集合 无序不重复
e={1,23,2,23,"haha",'ha'}
print(e)
e.add('ss')
e.update({10,'sec',1})
print(e)
f={1,'张卫健','刘德华'}
#取交集
print(e & f)
#取并集
print(e | f)
#取差集
print(e-f)
e.remove(23)
print(e)
e1=e.pop()
print(e)
print(e1)
print('a' in e)
print ('a' not in e)