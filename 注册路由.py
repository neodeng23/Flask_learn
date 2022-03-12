from flask import Flask

'''
我们安装Flask时，它会在Python解释器中创建一个flask包，我们可以通过
flask包的构造文件导入所有开放的类和函数。我们先从flask包导入Flask类，这
个类表示一个Flask程序。实例化这个类，就得到我们的程序实例app：
'''

app = Flask(__name__)

'''
传入Flask类构造方法的第一个参数是模块或包的名称，我们应该使用特殊变量
__name__。Python会根据所处的模块来赋予__name__变量相应的值，对于我们的
程序来说（app.py），这个值为app
'''


@app.route('/')
def index():
    """
    route（）装饰器的第一个参数是URL规则，用字符串表示，必须以斜杠（/）开始。
    这里的URL是相对URL（又称为内部URL），即不包含域名的URL。

    以域名www.helloflask.com 为例，“/”对应的是根地址（即www.helloflask.com），
    如果把URL规则改为“/hello”，则实际的绝对地址（外部地址）是www.helloflask.com/hello
    """

    return '<h1>Hello Flask!</h1>'


@app.route('/hi')
@app.route('/hello')
def say_hello():
    """
    可以绑定多个url
    """
    return '<h1>Hello, Flask!</h1>'


@app.route('/greet/<name>')
def greet(name):
    """
    动态URL
    我们不仅可以为视图函数绑定多个URL，还可以在URL规则中添加变量部分，使用“<变量名>”的形式表示。Flask处理请求时会把变量传入视图函数，
    所以我们可以添加参数获取这个变量值
    """
    return '<h1>Hello, %s!</h1>' % name


"""
为url添加默认值，以下两种方法效果相同

"""
@app.route('/greet', defaults={'name': 'Programmer'})
@app.route('/greet/<name>')
def greet(name):
    return '<h1>Hello, %s!</h1>' % name


@app.route('/greet')
@app.route('/greet/<name>')
def greet(name='Programmer'):
    return '<h1>Hello, %s!</h1>' % name


@app.route('goback/<int:year>')
def go_back(year):
    """
    URL转换器，string,int,float,path,
    any:匹配一系列给定值中的一个元素，<any（value1，value2，...）：变量名>
    uuid：UUID字符串
    """
    return '<p>Welcome to %d!</p>' % (2018 - year)