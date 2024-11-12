'''给定年月日判断过了多少天'''
import datetime

year=int(input('年:'))
mon=int(input('月:'))
day=int(input('日:'))

date1=datetime.date(year=year,month=mon,day=day)
date2=datetime.date(year=year,month=1,day=1)
days=(date1-date2).days+1
print(days)