import os

'''os 模块
./  当前目录
../ 父级目录

'''
print(123)
#获取当前文件绝对路径，包括文件名
abs_path=os.path.abspath(__file__)
print(abs_path)

#获取绝对路径，无当前文件名，只有路径
os_cwd=os.getcwd()
print(os_cwd)

#查询指定路径下所有文件及目录名，如果不传参数，默认为当前目录
dir_list=os.listdir('../')
print(dir_list)

#判断传入的是否是文件
print(os.path.isfile('./os模块.py'))
#判断传入的是否是目录
print(os.path.isdir('./test_file_data'))

#h获取父级目录
print(os.path.dirname(os.path.dirname(abs_path)))
#执行程序或命令command  在Windows系统中，返回值为cmd的调用返回信息
print(os.system('C:\\Users\\admin\Pictures\\v2-8d9b0e284d1a77099140cf2ed0a9f122_hd'))
print(os.system('ping  baidu.com'))

'''os.system 乱码，可以设置 File Encodings  Global Encoding  设置为GBK   '''