import datetime
# 获取当前时间
now = datetime.datetime.now()
# 获取今天零点
zeroToday = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
# 获取23:59:59
lastToday = zeroToday + datetime.timedelta(hours=23, minutes=59, seconds=59)
# 获取前一天的当前时间
yesterdayNow = now - datetime.timedelta(hours=23, minutes=59, seconds=59)
# 获取明天的当前时间
tomorrowNow = now + datetime.timedelta(hours=23, minutes=59, seconds=59)

print('时间差', datetime.timedelta(hours=23, minutes=59, seconds=59))
print('当前时间', now)
print('今天零点', zeroToday)
print('获取23:59:59', lastToday)
print('昨天当前时间', yesterdayNow)
print('明天当前时间', tomorrowNow)
print('时间格式化',now.strftime('%Y-%m-%d %H:%M:%S'))

