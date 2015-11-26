from flask import Flask, render_template, request, url_for, redirect, session
import sparkfunction

app = Flask(__name__)


@app.route('/')
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


@app.route("/user", methods=['DELETE'])
def Logout():
    user.login = False
    return None


if __name__ == '__main__':
    # TODO: add algo to make the tiles here
    app.debug = True
    app.run()
