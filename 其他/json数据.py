'''
json.dumps() 将 Python 对象转换为 JSON 字符串，并返回该字符串。而 json.dump() 将 Python 对象转换为 JSON 字符串，并将该字符串写入文件。

：json.dumps 序列化时默认使用的ascii编码，想输出真正的中文需要指定ensure_ascii=False：更深入分析，是应为dJSON object 不是单纯的unicode实现，而是包含了混合的unicode编码以及已经用utf-8编码之后的字符串。
'''
import json

dict1={'天王':'天王盖地虎',
       '宝塔':'宝塔镇河妖'}
#ensure_ascii=False 不写这个中文乱码
print(json.dumps(dict1,ensure_ascii=False))
# print(json.dump(dict1))

f=open('./test_file_data/a.txt','w')
print(type(f))
f.close()

with open('./test_file_data/a.txt','w') as f:
       res=json.dump(dict1,f,ensure_ascii=False)
       print(res)

with open('./test_file_data/a.txt','r') as f1:
       res=json.load(f1)
       print(res)