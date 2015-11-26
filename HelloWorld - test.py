from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello_world():
    return "Hello World, this is a god-damned app"


@app.route('/testpage')
def testpage():
    return "This is a testpage"


if __name__ == '__main__':
    app.debug = True
    app.run()
