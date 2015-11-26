from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello_world():
    return "Flask(__name__)"


@app.route('/testpage')
def testpage():
    return "This is a testpage"


if __name__ == '__main__':
    app.debug = True
    app.run()
