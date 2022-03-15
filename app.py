import click
import json
from flask import Flask, request, redirect, url_for, abort, make_response, jsonify, session, render_template, flash
from func import *
import data

app = Flask(__name__)
# app = Flask(__name__,template_folder="templates",static_folder="static")
"""
static_folder = 'static',  # 静态文件目录的路径 默认当前项目中的static目录
static_host = None,  # 远程静态文件所用的Host地址,默认为空
static_url_path = None,  # 静态文件目录的url路径 默认不写是与static_folder同名,远程静态文件时复用
# host_matching是否开启host主机位匹配,是要与static_host一起使用,如果配置了static_host, 则必须赋值为True
# 这里要说明一下,@app.route("/",host="localhost:5000") 就必须要这样写
# host="localhost:5000" 如果主机头不是 localhost:5000 则无法通过当前的路由
host_matching = False,  # 如果不是特别需要的话,慎用,否则所有的route 都需要host=""的参数
subdomain_matching = False,  # 理论上来说是用来限制SERVER_NAME子域名的,但是目前还没有感觉出来区别在哪里
template_folder = 'templates'  # template模板目录, 默认当前项目中的 templates 目录
instance_path = None,  # 指向另一个Flask实例的路径
instance_relative_config = False  # 是否加载另一个实例的配置
root_path = None  # 主模块所在的目录的绝对路径,默认项目目录
"""

app.config['SECRET_KEY'] = '123456'
"""
{
    'DEBUG': False,  # 是否开启Debug模式
    'TESTING': False,  # 是否开启测试模式
    'PROPAGATE_EXCEPTIONS': None,  # 异常传播(是否在控制台打印LOG) 当Debug或者testing开启后,自动为True
    'PRESERVE_CONTEXT_ON_EXCEPTION': None,  # 一两句话说不清楚,一般不用它
    'SECRET_KEY': None,  # 之前遇到过,在启用Session的时候,一定要有它
    'PERMANENT_SESSION_LIFETIME': 31,  # days , Session的生命周期(天)默认31天
    'USE_X_SENDFILE': False,  # 是否弃用 x_sendfile
    'LOGGER_NAME': None,  # 日志记录器的名称
    'LOGGER_HANDLER_POLICY': 'always',
    'SERVER_NAME': None,  # 服务访问域名
    'APPLICATION_ROOT': None,  # 项目的完整路径
    'SESSION_COOKIE_NAME': 'session',  # 在cookies中存放session加密字符串的名字
    'SESSION_COOKIE_DOMAIN': None,  # 在哪个域名下会产生session记录在cookies中
    'SESSION_COOKIE_PATH': None,  # cookies的路径
    'SESSION_COOKIE_HTTPONLY': True,  # 控制 cookie 是否应被设置 httponly 的标志，
    'SESSION_COOKIE_SECURE': False,  # 控制 cookie 是否应被设置安全标志
    'SESSION_REFRESH_EACH_REQUEST': True,  # 这个标志控制永久会话如何刷新
    'MAX_CONTENT_LENGTH': None,  # 如果设置为字节数， Flask 会拒绝内容长度大于此值的请求进入，并返回一个 413 状态码
    'SEND_FILE_MAX_AGE_DEFAULT': 12,  # hours 默认缓存控制的最大期限
    'TRAP_BAD_REQUEST_ERRORS': False,
    # 如果这个值被设置为 True ，Flask不会执行 HTTP 异常的错误处理，而是像对待其它异常一样，
    # 通过异常栈让它冒泡地抛出。这对于需要找出 HTTP 异常源头的可怕调试情形是有用的。
    'TRAP_HTTP_EXCEPTIONS': False,
    # Werkzeug 处理请求中的特定数据的内部数据结构会抛出同样也是“错误的请求”异常的特殊的 key errors 。
    # 同样地，为了保持一致，许多操作可以显式地抛出 BadRequest 异常。
    # 因为在调试中，你希望准确地找出异常的原因，这个设置用于在这些情形下调试。
    # 如果这个值被设置为 True ，你只会得到常规的回溯。
    'EXPLAIN_TEMPLATE_LOADING': False,
    'PREFERRED_URL_SCHEME': 'http',  # 生成URL的时候如果没有可用的 URL 模式话将使用这个值
    'JSON_AS_ASCII': True,
    # 默认情况下 Flask 使用 ascii 编码来序列化对象。如果这个值被设置为 False ，
    # Flask不会将其编码为 ASCII，并且按原样输出，返回它的 unicode 字符串。
    # 比如 jsonfiy 会自动地采用 utf-8 来编码它然后才进行传输。
    'JSON_SORT_KEYS': True,
    #默认情况下 Flask 按照 JSON 对象的键的顺序来序来序列化它。
    # 这样做是为了确保键的顺序不会受到字典的哈希种子的影响，从而返回的值每次都是一致的，不会造成无用的额外 HTTP 缓存。
    # 你可以通过修改这个配置的值来覆盖默认的操作。但这是不被推荐的做法因为这个默认的行为可能会给你在性能的代价上带来改善。
    'JSONIFY_PRETTYPRINT_REGULAR': True,
    'JSONIFY_MIMETYPE': 'application/json',
    'TEMPLATES_AUTO_RELOAD': None,
}
"""

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


@app.route('/hello')
def say_hello():
    """
    可以绑定多个url
    """
    return '<h1>go go go, Flask!</h1>'


@app.route('/hi')
def hi():
    """
    重定向到/hello

    """
    return redirect(url_for('say_hello'))


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


@app.route('/watchlist')
def watchlist():
    user = data.user
    movies = data.movies
    return render_template('watchlist.html', user=user, movies=movies)


@app.template_global()
def bar():
    """
    注册为全局函数
    """
    return 'I am bar.'


@app.route('/flash')
def just_flash():
    flash('I am flash, who is looking for me?')
    return redirect(url_for('get_cookie_demo'))


@app.route('/basic', methods=['GET', 'POST'])
def basic():
    form = LoginForm() # GET + POST
    if request.method == 'POST' and form.validate():
        # 处理POST请求
        return render_template('forms/basic.html', form=form) # 处理GET请求


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
