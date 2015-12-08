from flask import Flask, render_template, request, url_for, redirect, session, Response
import sparkfunction
import PhotonCall
import mahjongStates_vFINAL
import subprocess
import time
import GcmBot
import uuid


app = Flask(__name__)

##################################################################
# SETUP GcmBot
##################################################################
xmpp = GcmBot.GcmBot(GcmBot.USERNAME, GcmBot.PASSWORD)
xmpp.register_plugin('xep_0184') # Message Delivery Receipts
xmpp.register_plugin('xep_0198') # Stream Management
xmpp.register_plugin('xep_0199')  # XMPP Ping

# Connect to the XMPP server and start processing XMPP stanzas.
gcm_connection =  xmpp.connect(('gcm.googleapis.com', 5235), use_ssl=True)

if gcm_connection:
    # Threaded, non blocking
    xmpp.process(block=False)



##################################################################
# ROUTING
##################################################################
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

@app.route("/gcm")
def gcmTest():
    message = {
        "to": GcmBot.iot_mahjong_s6,
        "message_id": uuid.uuid1().urn[9:],
        "data":
            {
                "number": "mobile number",
                "message": "Meow meow meow"
                # "message": u"odoo 测试 GCMSMS 网关:sleepxmpp",
            },
        "time_to_live": 600,
        "delay_while_idle": True,
        "delivery_receipt_requested": True
    }
    xmpp.send_gcm_message(message)
    return "trying"


@app.route("/game")
def game():
    mahjongStates_vFINAL.startthegoddamnedgame()
    return "Game Started!"


@app.route("/update")
def update():
    action = request.args.get('action', '')
    if action == '':
        action = "on"
    PhotonCall.sendToPhoton(action)
    return "Done! - Information Sent"


# Testing some stuff - if its possible to show the current state on the
# webserver
@app.route('/yeild')
def yeild():
    def inner():
        proc = subprocess.Popen(
            # call something with a lot of output so we can see it
            ["python", "mahjongStates_vFINAL.py"],
            shell=False,
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
