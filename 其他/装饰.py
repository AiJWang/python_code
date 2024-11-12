'''@property 让方法可以像属性一样被调用，不需要奥加() ,必须有返回值'''


class User:
    def __init__(self):
        self.__age=10

    def getage(self):
        return self.__age

    @property
    def age(self):
        return self.__age

    @age.setter
    def setage(self,age):
        self.__age=age


if __name__ == '__main__':
    u=User()
    print(u.getage())
    print(u.age)
    u.age=12
    print(u.age)