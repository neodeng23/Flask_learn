"""
除了Flask内置的flask run等命令，我们也可以自定义命令。在虚拟环境安装Flask后，包含许多内置命令的flask脚本就可以使用了。在前面我们已经接触了很多flask命令，比如运行服务器的flask run，启动shell的flask shell。
通过创建任意一个函数，并为其添加app.cli.command（）装饰器，我们就可以注册一个flask命令。
"""

# @app.cli.command()
# def hello():
#     click.echo('Hello, Human!')

