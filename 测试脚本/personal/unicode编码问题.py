
# 字符串时unicode转义序列，解码就好了
if __name__=='__main__':
    text = r'\u6210\u529f'
    ccc = bytes(text, 'utf-8').decode('unicode-escape')
    print(ccc)
