'''在通过requests.post()进行POST请求时，传入报文的参数有两个，一个是data，一个是json。

data与json既可以是str类型，也可以是dict类型。

区别：

1、不管json是str还是dict，如果不指定headers中的content-type，默认为application/json

2、data为dict时，如果不指定content-type，默认为application/x-www-form-urlencoded，相当于普通form表单提交的形式

3、data为str时，如果不指定content-type，默认为text/plain

4、json为dict时，如果不指定content-type，默认为application/json

5、json为str时，如果不指定content-type，默认为application/json

6、用data参数提交数据时，request.body的内容则为a=1&b=2的这种形式，用json参数提交数据时，request.body的内容则为'{“a”: 1, “b”: 2}’的这种形式'''