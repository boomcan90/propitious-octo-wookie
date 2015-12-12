from flask import Flask, render_template, request, url_for, redirect, session, Response
import sparkfunction
import photon_call
from mahjong_stm_objects import *
import mahjong_stm_main
import subprocess
import time
import gcm_bot
import uuid
import redis
import os
import redis
import json

#Redis
r = redis.from_url(os.environ.get("REDIS_URL"))
r.set('temp_photon_data', 'nothing yet');

#Publish subscribe
from pubsub import pub

app = Flask(__name__)

##################################################################
# GLOBAL OBJECTS
##################################################################
online_clients = []

user1_update_count = 0
user2_update_count = 0

user1_tiles = None
user2_tiles = None

##################################################################
# SETUP GcmBot. Basically you have an object called "xmpp"
##################################################################
xmpp = gcm_bot.GcmBot(gcm_bot.USERNAME, gcm_bot.PASSWORD)
xmpp.register_plugin('xep_0184') # Message Delivery Receipts
xmpp.register_plugin('xep_0198') # Stream Management
xmpp.register_plugin('xep_0199')  # XMPP Ping

# Connect to the XMPP server and start processing XMPP stanzas.

# xmpp.startConnection()


# Keyboard Interrupt for XMPP thread
import signal
import sys
import time

def signal_handler(signal, frame):
    print 'You pressed Ctrl+C!'
    xmpp.disconnect()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

##################################################################
# Subscribe to GcmBot's updates
# 1. Like a message from android clients was received
# 2. The sky fell
##################################################################
def gcm_updates(arg1, arg2=None):
    print "gcm update: ", arg1
    print "more info: ", arg2

# function_that_wants_updates, "string"
pub.subscribe(gcm_updates, 'clientMessageReceived')

##################################################################
# Photon updates
##################################################################
@app.route('/photonUpdate', methods=['POST'])
def photonUpdate():
    content = request.get_json(silent=True, force=True)
    content.pop("data", None)
    print content
    print "json dump\n"
    print json.dumps(content)
    print "\n"
    r.set('temp_photon_data', json.dumps(content))
    print "json load\n"
    print json.loads(r.get('temp_photon_data'))
    print "\n"
    return "ok"

@app.route('/latestPhotonUpdate', methods=['GET'])
def photonLastestUpdate():
    resp = Response(response=json.loads(r.get('temp_photon_data')),
    status=200, \
    mimetype="application/json")
    return resp


##################################################################
# Create statemachine
##################################################################



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


##################################################################
# Example of how you would use the XMPP object to send message.
##################################################################
@app.route("/gcm")
def gcmTest():
    message = {
        "to": GcmBot.iot_mahjong_s6,
        "message_id": uuid.uuid1().urn[9:],
        "data":
            {
                "number": "mobile number",
                "message": "Meow meow meow"
            },
        "time_to_live": 600,
        "delay_while_idle": True,
        "delivery_receipt_requested": True
    }
    xmpp.send_gcm_message(message)
    return "SENT MESSAGE TO ANDROID VIA GCM!"

##################################################################
# Register Client
##################################################################
@app.route('/api/register', methods=['POST'])
def registerClient():
    content = request.get_json(silent=True)
    # if token is provided
    # if token is not in list, add to list
    if content.token:
        for i in online_clients:
            if i != content.token:
                online_clients.append(content.token)
    print content
    return "Registration with: ", content


##################################################################
# Trial of starting the game
##################################################################
@app.route("/game")
def game():
    mahjongStates_vFINAL.startthegoddamnedgame()
    return "Game Started!"


##################################################################
# Register Client
##################################################################
@app.route("/update")
def update():
    action = request.args.get('action', '')
    if action == '':
        action = "0"
    result = PhotonCall.sendToPhoton(action)
    return result

@app.route("/getpos")
def get_pos():
    pid = request.args.get('pid', '')
    if pid == '':
        pid = None
    result = PhotonCall.getFromPhoton(pid)
    return result

@app.route("/photondemo")
def demo_page():
    return render_template('./index.html')

# Testing some stuff - if its possible to show the current state on the
# webserver
@app.route('/yieldd')
def yieldd():
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
