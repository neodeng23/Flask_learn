import click
import json
from flask import Flask, request, redirect, url_for, abort, make_response, jsonify, session

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
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


@app.route('/foo')
def foo():
    """
    Flask通过引入Python标准库中的json模块（或simplejson，如果可用）为程序提供了JSON支持。
    你可以直接从Flask中导入json对象，然后调用dumps（）方法将字典、列表或元组序列化（serialize）为JSON字符串
    """
    data = {
        'name': 'Grey Li',
        'gender': 'male'
    }
    response = make_response(json.dumps(data))
    response.mimetype = 'application/json'
    return response


@app.route('/foo_1')
def foo_1():
    """
    不过我们一般并不直接使用json模块的dumps（）、load（）等方法，因为Flask通过包装这些方法提供了更方便的jsonify（）函数。
    借助jsonify（）函数，我们仅需要传入数据或参数，它会对我们传入的参数进行序列化，转换成JSON字符串作为响应的主体，然后生成一个响应对象，并且设置正确的MIME类型。
    jsonify（）函数接收多种形式的参数。你既可以传入普通参数，也可以传入关键字参数。如果你想要更直观一点，也可以像使用dumps（）方法一样传入字典、列表或元组
    jsonify（）函数默认生成200响应，你也可以通过附加状态码来自定义响应类型，
    """
    return jsonify(name='Grey Li', gender='male'), 200


@app.route('/set/<name>')
def set_cookie_demo(name):
    """
    将URL中的name变量的值设置到名为name的cookie里
    在这个make_response（）函数中，我们传入的是使用redirect（）函数生成的重定向响应。
    set_cookie视图会在生成的响应报文首部中创建一个Set-Cookie字段，即“Set-Cookie：name=Grey；Path=/”。
    """
    response = make_response(redirect(url_for('hello_1')))
    response.set_cookie('name', name)
    return response


@app.route('/hello11')
def get_cookie_demo():
    """
    Cookie可以通过请求对象的cookies属性读取。在修改后的hello视图中，如果没有从查询参数中获取到name的值，就从Cookie中寻找
    """
    name = request.args.get('name')
    if name is None:
        name = request.cookies.get('name', 'Human')
        response = '<h1>Hello, %s!</h1>' % name
        # 根据用户认证状态返回不同的内容
        if 'logged_in' in session:
            response += '[Authenticated]'
        else:
            response += '[Not Authenticated]'
        return response


@app.route('/login')
def login():
    session['logged_in'] = True  # 写入session
    return redirect(url_for('get_cookie_demo'))


@app.route('/admin')
def admin():
    """
        未登录就403
    """
    if 'logged_in' not in session:
        abort(403)
    return 'Welcome to admin page.'


@app.route('/logout')
def logout():
    """
        登出
    """
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('hello'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
