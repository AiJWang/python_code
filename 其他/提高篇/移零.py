
'''
* 给定一个数组，将数组中所有0移动到数组末尾，将非0数字保持相对顺序
* 例： 输入 [0,2,0,1,6,0]
*     输出 [2,1,6,0,0,0]
'''

def move_z(list):
    j=0
    for i in list:
       if i!=0:
           list[j]=i
           j+=1
    for i in range(j,len(list)):
        list[i]=0

list=[0,2,0,1,6,0]

move_z(list)
print(list)