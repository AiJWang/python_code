a=int(input("请输入数字"))
while a>0:
    if a<5:
        continue
    print(a)
    a=a-1
    if a>1000:
        break