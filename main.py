# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from functools import wraps

import pytest


class A:

    def swrapper(fn):
        @wraps(fn)
        def dec_inner(self,**kwargs):
            kwargs['zhangsan'] = 2222
            fn(self,**kwargs)

        return dec_inner

    @swrapper
    def playlol(self,**kwargs):

        print(kwargs['zhangsan'])


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(abs(+323.0-323.0))
    assert abs(+323.0-323.0)<1

    print(100152190-100102195.0)
    # print(u'\\u0e4f\\u032f\\u0361\\u0e4f'.decode('unicode-escape'))
    # text = r'\u6210\u529f'
    # ccc = bytes(text, 'utf-8').decode('unicode-escape')
    # print(ccc)
    # # print(\u6210\u529f.decode('unicode-escape'))
    # print('-' * 30)
    # aa=A()
    # s={'zhangsan':12}
    # aa.playlol(zhangsan='2sss')
    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
