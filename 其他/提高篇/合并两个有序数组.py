'''合并两个有序数组'''


def combain_arr(list1,list2):
    a=0
    totallen=len(list1)+len(list2)
    list3=list()
    i,j=0,0
    while a<totallen:
        if i>=len(list1):
            list3.append(list2[j])
            j+=1
        elif j>=len(list2):
            list3.append(list1[i])
            i+=1
        elif list1[i]<=list2[j]:
            list3.append(list1[i])
            i+=1
        elif list1[i]>list2[j]:
            list3.append(list2[j])
            j+=1
        a+=1
    return list3
list1=[1,3,5]
list2=[2,4,6,8,10]

res=combain_arr(list1,list2)
print(res)