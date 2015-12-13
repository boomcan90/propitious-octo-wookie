from flask import Flask, render_template, request, url_for, redirect, session, Response
import sparkfunction
import photon_call
from mahjong_stm_objects import *
# import mahjong_stm_main
import subprocess
import time
import gcm_bot
import uuid
import redis
import os
import redis
import json
import jsonpickle

#Publish subscribe
from pubsub import pub

app = Flask(__name__)

##################################################################
# GLOBAL OBJECTS
##################################################################
#Redis
redis_url = os.getenv('HEROKU_REDIS_MAUVE_URL', 'redis://localhost:6379')
r = redis.from_url(redis_url)
r.set('temp_photon_data', 'nothing yet')


#Hacky user management and tiles
r.set('online_clients', 0)

r.set('user1_live_tiles', jsonpickle.dumps({}))
r.set('user2_live_tiles', jsonpickle.dumps({}))

# orange: pirate, morphing, zombie
user1_tiles = ["250040000347343337373737", "2b002d000447343233323032", "3b003d000347343339373536"]
# green: raptor, hunter, dentist
user2_tiles = ["210039000347343337373737", "1c003e000d47343432313031", "37001c001347343432313031"]

temp_user_tiles = {}
for token in user1_tiles:
    temp_user_tiles[token] = Tile(token=token)
r.set('user1_live_tiles', jsonpickle.dumps(temp_user_tiles))


temp_user_tiles = {}
for token in user2_tiles:
    temp_user_tiles[token] = Tile(token=token)
r.set('user2_live_tiles', jsonpickle.dumps(temp_user_tiles))

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
# PHOTON UPDATES
##################################################################

# Handles each tile's update and sets it in redis (triplets)
def tileUpdateHandler(tile_data):
    tiles1 = jsonpickle.loads(r.get('user1_live_tiles'))
    tiles2 = jsonpickle.loads(r.get('user2_live_tiles'))
    print "got tiles"
    if "source" in tile_data:
        print "source"
        if tile_data["source"] in user1_tiles:
            print "updating tiles1"
            tiles1[tile_data["source"]].orientation = tile_data["orientation"]
            tiles1[tile_data["source"]].kind = tile_data["tile"] # update tile kind with "tile from photon"
            tiles1[tile_data["source"]].x = tile_data["x"]
            tiles1[tile_data["source"]].y = tile_data["y"]
            tiles1[tile_data["source"]].z = tile_data["z"]
            r.set('user1_live_tiles', jsonpickle.dumps(tiles1))
            print "done with tiles1"
            if tiles1[tile_data["source"]].orientation != tile_data["orientation"]:
                #updates
                pass

        elif tile_data["source"] in user2_tiles:
            print "updating tiles2"
            tiles2[tile_data["source"]].orientation = tile_data["orientation"]
            tiles2[tile_data["source"]].kind = tile_data["tile"] # update tile kind with "tile from photon"
            tiles2[tile_data["source"]].x = tile_data["x"]
            tiles2[tile_data["source"]].y = tile_data["y"]
            tiles2[tile_data["source"]].z = tile_data["z"]
            r.set('user2_live_tiles', jsonpickle.dumps(tiles2))
            print "done with tiles2"
            if tiles2[tile_data["source"]].orientation != tile_data["orientation"]:
                #updates
                pass
        else:
            print "error occurred while processing tile data"

@app.route('/photonUpdate', methods=['POST'])
def photonUpdate():
    content = request.get_json(silent=True, force=True)
    # remove the additional property particle servers provide
    content.pop("data", None)
    print content
    r.set('temp_photon_data', json.dumps(content))

    # more updating to be done
    tileUpdateHandler(content)
    return "ok"

@app.route('/latestPhotonUpdate', methods=['GET'])
def photonLastestUpdate():
    action = request.args.get('action', '')
    data = r.get('user1_live_tiles')
    if action != '':
        data = r.get('user2_live_tiles')
    resp = Response(response=data,
    status=200, \
    mimetype="application/json")
    return resp


##################################################################
# ROUTING
##################################################################
@app.route('/')
def main():
    # return "test"
    return render_template('./sparktemplate.html', tempdata=1, utimedata=1,
                           ledstatus=1, authbool=True)

##################################################################
# PARTICLE LED TEST
##################################################################
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
    # mahjongStates_vFINAL.startthegoddamnedgame()
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
