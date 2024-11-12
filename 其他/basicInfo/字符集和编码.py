'''
一个字节8位
ascii ==> 编了128个符号，包括字母 数字，标点，特殊符号等  是符合美国人的编码 01111111  1byte=8bit

美国有开了一套标准 ANSI
ansi==》 就是扩展了ascii 变为 16bit  2byte，00000000 01111111 （后面是ascii的），然后其他地区在前面扩展就行

到了中国 用的 gbk   在日本又是另一套了，并不兼容，所以国际组织把所有国家文字都重新编码 就是 unicode

unicode：万国码，但是unicode是4个字节，浪费空间，所以又出了 utf，就是可变长度的unicode，可进行数据传输和存储

utf-8：最短字节长度是8位
    英文：8bit  1byte
    欧洲文字：16bit 2byte
    中文：24bit  3byte

总结：
    ascii：8bit 1byte（美国人语言系统）
    gbk：16bit  2byte （中文编码，windows默认编码）
    utf-8：最短字节长度是8位
    英文：8bit  1byte
    欧洲文字：16bit 2byte
    中文：24bit  3byte

    utf-8和gbk不能直接转化，因为gbk来源于ascii，而utf-8源于unicode，是两套标准

    bytes：
        程序员遇见的数据最终单位都是字节 byte
'''

s='王爱军'
#用gbk进行编码
s1=s.encode('gbk')
#用utf-8进行编码
s2=s.encode('utf-8')
print(s1)
print(s2)

#把gbk字节转化为utf-8的
#先解码
ss=s1.decode('gbk')
print(ss)
ss2=ss.encode('utf-8')
print(ss2)