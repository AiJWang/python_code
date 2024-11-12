import pytest


class Testmark:
    @pytest.mark.parametrize('args',['12','we'])
    def test_a(self,args):
        print(args)

    @pytest.mark.parametrize('name,age',[['huanfeng',23],['night',15]])
    def testb(self,name,age):
        print(name,age)

if __name__ == '__main__':
    pytest.main(['-vs'])