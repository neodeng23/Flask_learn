import click
from flask import Flask, request, redirect, url_for, abort

app = Flask(__name__)

"""
一般来说，在执行flask run命令运行程序前，我们需要提供程序实例所在模块的位置。我们在上面可以直接运行程序，是因为Flask会自动探测程序实例，自动探测存在下面这些规则
·从当前目录寻找app.py和wsgi.py模块，并从中寻找名为app或application的程序实例。
·从环境变量FLASK_APP对应的值寻找名为app或application的程序实例。

因为我们的程序主模块命名为app.py，所以flask run命令会自动在其中寻找程序实例。如果你的程序主模块是其他名称，比如hello.py，那么需要设置环境变量FLASK_APP，将包含程序实例的模块名赋值给这个变量。
Linux或macOS系统使用export命令：
    $ export FLASK_APP=hello
在Windows系统中使用set命令：
    > set FLASK_APP=hello
    
启动：
    flask run --host=0.0.0.0
"""

FLASK_RUN_HOST = "0.0.0.0"
FLASK_RUN_PORT = "2400"


@app.route('/hi')
@app.route('/hello')
def say_hello():
    """
    可以绑定多个url
    """
    return '<h1>go go go, Flask!</h1>'


@app.route('/hello_1', methods=['GET', 'POST'])
def hello_1():
    """
    我们可以在app.route（）装饰器中使用methods参数传入一个包含监听的HTTP方法的可迭代对象。
    """
    return '<h1>Hello, Flask!</h1>'


@app.route('/hello_2')
def hello_2():
    """
    视图函数可以返回最多由三个元素组成的元组：响应主体、状态码、首部字段

    """
    print("ok")
    return '', 302, {'Location', 'http://www.example.com'}


@app.route('/hello_3')
def hello_3():
    """
    重定向

    """
    return redirect('http://www.baidu.com')


@app.cli.command()
def hello():
    """
    借助click模块的echo（）函数，我们可以在命令行界面输出字符。命令函数文档字符串则会作为帮助信息显示（flask hello--help）。在命令行下执行flask hello命令就会触发这个hello（）函数：
    """
    print("this is hello")
    click.echo('Hello, Human!')


@app.route('/hi')
def hi():
    """
    重定向到/hello

    """
    return redirect(url_for('say_hello'))


@app.before_request
def do_something():
    print("do it before request")
    pass  # 这里的代码会在每个请求处理前执行


@app.route('/404')
def not_found():
    abort(404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)