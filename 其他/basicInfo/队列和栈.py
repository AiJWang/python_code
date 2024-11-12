

'''队列：先进先出,可以用deque实现'''
from cgitb import reset
from collections import deque
from inspect import stack
from turtledemo.penrose import start

#进队列
queue=deque()
queue.append(1)
queue.append(2)
queue.append(3)
queue.append(4)
print(queue)
#出队列
res=queue.popleft()
print(res)
res=queue.popleft()
print(res)
res=queue.popleft()
print(res)
res=queue.popleft()
print(res)


'''栈，先进后出，可以用列表实现'''
#入栈
stack=[]
stack.append(1)
stack.append(2)
stack.append(3)
print(stack)
#出栈
re=stack.pop()
print(re)
re=stack.pop()
print(re)
re=stack.pop()
print(re)