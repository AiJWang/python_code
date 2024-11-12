from locale import strcoll

list1=['梅花10','梅花9','梅花8']
def judge_tonghua(list1):
    huase=list1[0][0:2]
    listc=[]
    for i in list1:
        if str(i).startswith(huase):
            if str(i).endswith('10'):
                listc.append(i[len(i)-2:len(i)])
            else:
                listc.append(i[len(i)-1])
        else:
            return False
    print(listc)
    print(type(listc[0]))
    if type(listc[0]) ==int and type(listc[1])==int and type(listc[2])==int:
        sorted(listc)
        return listc[0]+1==listc[1] and listc[0]+2==listc[2]
    else:
        pass

print(judge_tonghua(list1))