'''��ͨ��requests.post()����POST����ʱ�����뱨�ĵĲ�����������һ����data��һ����json��

data��json�ȿ�����str���ͣ�Ҳ������dict���͡�

����

1������json��str����dict�������ָ��headers�е�content-type��Ĭ��Ϊapplication/json

2��dataΪdictʱ�������ָ��content-type��Ĭ��Ϊapplication/x-www-form-urlencoded���൱����ͨform���ύ����ʽ

3��dataΪstrʱ�������ָ��content-type��Ĭ��Ϊtext/plain

4��jsonΪdictʱ�������ָ��content-type��Ĭ��Ϊapplication/json

5��jsonΪstrʱ�������ָ��content-type��Ĭ��Ϊapplication/json

6����data�����ύ����ʱ��request.body��������Ϊa=1&b=2��������ʽ����json�����ύ����ʱ��request.body��������Ϊ'{��a��: 1, ��b��: 2}����������ʽ'''