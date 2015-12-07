from flask import Flask, render_template, request, url_for, redirect, session, Response
import sparkfunction
import PhotonCall
import mahjongStates_vFINAL
import subprocess
import time

app = Flask(__name__)


@app.route('/')
def main():
    # return "test"
    return render_template('./sparktemplate.html', tempdata=1, utimedata=1,
                           ledstatus=1, authbool=True)


@app.route('/dataNow')
def DataNow():
    dataDict = sparkfunction.VarUpdate("delimOT")
    dataVals = dataDict.split(";")
    tempdata = dataVals[0]
    ledstatus = ledsparkvar(int(dataVals[1]))
    utimedata = dataVals[2] + " Days, " + dataVals[3] + \
        ":" + dataVals[4] + ":" + dataVals[5]

    authcookie = False
    if 'authuser' in session:
        authcookie = True
    if (request.args.get('auth') == 'xxx') or (authcookie):
        authbool = True
    else:
        authbool = False
    return render_template('sparktemplate.html', tempdata=tempdata,
                           utimedata=utimedata, ledstatus=ledstatus,
                           authbool=authbool)


@app.route('/led', methods=['POST'])
def LEDChange():
    sparkfunction.sparkLED(request.form['LED'])
    session['authuser'] = 'xxx'
    session.permanent = True
    return redirect('./')


def ledsparkvar(ledstatusInt):
    if ledstatusInt == 1:
        ledstatus = "On"
    elif ledstatusInt == 0:
        ledstatus = "Off"
    else:
        ledstatus = "LED Error"
    return ledstatus


@app.route("/game")
def startgame(*vars):
    # TODO: Things to add:
    mahjongStates_vFINAL()
    return "Game Started!"


@app.route("/update")
def update():
    PhotonCall.sendToPhoton("led")
    return "Done! - Information Sent"


# Testing some stuff - if its possible to show the current state on the
# webserver
@app.route('/yield')
def index():
    def inner():
        proc = subprocess.Popen(
            # call something with a lot of output so we can see it
            [mahjongStates_vFINAL()],
            shell=True,
            stdout=subprocess.PIPE
        )

        for line in iter(proc.stdout.readline, ''):
            # Don't need this just shows the text streaming
            time.sleep(1)
            yield line.rstrip() + '<br/>\n'

    # text/html is required for most browsers to show th$
    return Response(inner(), mimetype='text/html')

if __name__ == '__main__':
    # TODO: add algo to make the tiles here
    app.run()
