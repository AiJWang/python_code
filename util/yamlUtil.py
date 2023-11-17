import os

import yaml


class YmlTuil:
    #读取yml文件
    def readYml(self):
        with open("../extract.yml",mode='r',encoding='utf-8') as f:
            value=yaml.load(stream=f,Loader=yaml.FullLoader)
            return value

    #写入yml文件
    def writeYml(self,data):
        with open("../extract.yml",mode='w',encoding='utf-8') as f:
            yaml.dump(data=data,stream=f)

    #清除yml文件
    def clearYml(self):
        with open("../extract.yml",mode='w',encoding='utf-8') as f:
            f.truncate()

if __name__=='__main__':
    YmlTuil().writeYml('data=2346')