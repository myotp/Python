from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Haha, Hello PyCharm + Google App Engine!'

if __name__ == '__main__':
    app.run()
