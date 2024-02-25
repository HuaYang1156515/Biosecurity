from flask import Flask

# 创建一个 Flask 应用程序实例
app = Flask(__name__)

# 为主页定义一个路由
@app.route('/')
def index():
    return '欢迎来到生物安全指南！'

# 根据需要定义其他路由及其对应的函数

# 运行 Flask 应用程序
if __name__ == '__main__':
    app.run(debug=True)
