# -*- coding: utf-8 -*-

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Haha, Hello PyCharm + Google App Engine! 中文显示'

if __name__ == '__main__':
    app.run()
