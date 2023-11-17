# pytest.fixtrue() 一般会与conftest.py 文件一起使用
#conftest.py 名称是固定的，功能如下：
#    1. 用于存放多个pytest.fixtrue() 方法，可以在多个py文件之间共享前置配置
#    2. conftest里面的方法用的时候不需要导入，直接使用即可
#    3、 congtest.py 可以有多个，可以有多个层级
import pytest

from util.yamlUtil import YmlTuil

#需要手动调用
@pytest.fixture(scope='function')
def connect_database():
    print("start connect database")
    yield
    print("close database")

#清除yaml文件 自动执行
@pytest.fixture(scope='session',autouse=True)
def clear_yml():
    YmlTuil().clearYml()