from flask import Flask, render_template, request, url_for, redirect, session, Response
import photon_call
from mahjong_stm_objects import *
from mahjong_stm_util import *
import mahjong_stm_main
import subprocess
import time
import gcm_bot
import uuid
import redis
import os
import redis
import json
import jsonpickle
import signal
import sys
import pytz
import datetime
import ciso8601
import grequests
from gcm import GCM

#Publish subscribe
from pubsub import pub
from pubsub.py2and3 import print_

app = Flask(__name__)

##################################################################
# LOGGING
##################################################################
import logging
from logging import StreamHandler


# only python 3.2 fixed a bug for %z for this
#naive_date = datetime.datetime.strptime("2015-12-13T03:34:53+00:00", "%Y-%m-%dT%H:%M:%S%z")
# ts = ciso8601.parse_datetime("2015-12-12T09:49:54.874Z")
# local_timezone = pytz.timezone('Asia/Singapore')
# date_converted = ts.astimezone(local_timezone)
# print(date_converted)   # 2013-10-21 08:44:08-07:00
# sys.stdout.flush()


redis_url = os.getenv('HEROKU_REDIS_MAUVE_URL', 'redis://localhost:6379')
r = redis.from_url(redis_url)

# orange: pirate, morphing, zombie
user1_tiles = ["250040000347343337373737", "2b002d000447343233323032", "3b003d000347343339373536"]
# green: raptor, hunter, dentist
user2_tiles = ["210039000347343337373737", "1c003e000d47343432313031", "37001c001347343432313031"]

@app.before_first_request
def initial_execution():
##################################################################
# GLOBAL OBJECTS
##################################################################
#Redis
    file_handler = StreamHandler()
    app.logger.setLevel(logging.DEBUG)  # set the desired logging level here
    app.logger.addHandler(file_handler)

    r.set('temp_photon_data', 'nothing yet')


    #Hacky user management and tiles
    r.set('online_clients', jsonpickle.dumps([]))

    r.set('listOfTiles', jsonpickle.dumps([]))

    r.set('user1_live_tiles', jsonpickle.dumps({}))
    r.set('user2_live_tiles', jsonpickle.dumps({}))

    r.set('user1_tiles', jsonpickle.dumps(user1_tiles))
    r.set('user2_tiles', jsonpickle.dumps(user2_tiles))

    temp_user_tiles = {}
    for token in user1_tiles:
        temp_user_tiles[token] = Tile(token=token)
    r.set('user1_live_tiles', jsonpickle.dumps(temp_user_tiles))


    temp_user_tiles = {}
    for token in user2_tiles:
        temp_user_tiles[token] = Tile(token=token)
    r.set('user2_live_tiles', jsonpickle.dumps(temp_user_tiles))

    # Hacky game state
    r.set('game_state', "nothing")

##################################################################
# SETUP GcmBot. Basically you have an object called "xmpp"
##################################################################
# xmpp = gcm_bot.GcmBot(gcm_bot.USERNAME, gcm_bot.PASSWORD)
# xmpp.register_plugin('xep_0184') # Message Delivery Receipts
# xmpp.register_plugin('xep_0198') # Stream Management
# xmpp.register_plugin('xep_0199')  # XMPP Ping

# Connect to the XMPP server and start processing XMPP stanzas.

# xmpp.startConnection()


# Keyboard Interrupt for XMPP thread
print "logging configured! & sys imported"
sys.stdout.flush()

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
# GAMEPLAY
##################################################################
#
# Sigh this really should be done better as an object
#
from transitions import Machine
def parseTileOrientation(tiles_dict):
    orientationList = []
    for key, value in tiles_dict.iteritems():
        # should be a tile
        orientationList.append(value.orientation)
    return orientationList

def parseTileKind(tiles_dict):
    kindList = []
    for key, value in tiles_dict.iteritems():
        # should be a tile
        kindList.append(value.kind)
    return kindList

##########################################################################

def send_gcm_message(message, reg_id):
    gcm = GCM("AIzaSyAf6J6MHvUlpnT_FIOoCws8Fs8oL7E0oOc")
    data = {'message': message}
    gcm.plaintext_request(registration_id=reg_id, data=data)

def player_update(tiles=None, extra=None):
    tiles1 = jsonpickle.loads(r.get('user1_live_tiles'))
    tiles2 = jsonpickle.loads(r.get('user2_live_tiles'))
    tiles1 = parseTileOrientation(tiles1)
    tiles2 = parseTileOrientation(tiles2)

    # recreate statemachine
    transitions = [
        # starting will expect both players to have tiles in a particular order
        { 'trigger': 'goto_p1_start', 'source': 'starting', 'dest': 'p1_start', 'before': 'send_p1_tile'},
        # { 'trigger': 'goto_p1_start', 'source': 'starting', 'dest': 'p1_start'},
        # send p1 tile and say please flip up your tiles
        { 'trigger': 'goto_p1_end', 'source': 'p1_start', 'dest': 'p1_end', 'before':'tell_p1_discard'},
        # { 'trigger': 'goto_p1_end', 'source': 'p1_start', 'dest': 'p1_end'},
        # say p1 now please discard a tile, flip 1 down
        { 'trigger': 'goto_p2_start', 'source': 'p1_end', 'dest': 'p2_start', 'before': 'send_p2_tile'},
        # { 'trigger': 'goto_p2_start', 'source': 'p1_end', 'dest': 'p2_start'},
        # send p2 tile and say please flip up your tiles
        { 'trigger': 'goto_p2_end', 'source': 'p2_start', 'dest': 'p2_end', 'before':'tell_p2_discard' },
        # { 'trigger': 'goto_p2_end', 'source': 'p2_start', 'dest': 'p2_end' },
        # say p2 now please discard a tile, flip 1 down
        { 'trigger': 'goto_p1_again', 'source': 'p2_end', 'dest': 'p1_start', 'before':'send_p1_tile' },
        # { 'trigger': 'goto_p1_again', 'source': 'p2_end', 'dest': 'p1_start'},
        # go back to 1 if nobody won
        { 'trigger': 'p1_wins', 'source': 'p1_start', 'dest': 'p1_winner' },
        { 'trigger': 'p2_wins', 'source': 'p2_start', 'dest': 'p2_winner' }
    ]

    # setup machine
    mahjong_game = Mahjong()
    machine = Machine(mahjong_game, states=['starting', 'p1_start', 'p1_end', 'p2_start', 'p2_end', 'p1_win', 'p2_win'], transitions=transitions, initial='starting')

    app.logger.debug(r.get('game_state'))


    machine.set_state(r.get('game_state'))

    app.logger.debug("current state:: " + mahjong_game.state)
    app.logger.debug(tiles1.count("1"))
    app.logger.debug(tiles2.count("1"))

    if mahjong_game.state == "starting":
        app.logger.debug("starting state evaluation")
        app.logger.debug("tiles1 1 count :: "  + str(tiles1.count("1")))
        app.logger.debug("tiles2 1 count :: "  + str(tiles2.count("1")))
        if tiles1.count("1") == 2 and tiles2.count("1") == 3:
            mahjong_game.goto_p1_start()
            app.logger.debug("going to p1start")
            r.set('game_state', mahjong_game.state)
    elif mahjong_game.state == "p1_start":
        app.logger.debug("P1 START STATE HOORAYYYY")
        if tiles1.count("1") == 3:
            app.logger.debug("P1 END STATE GOING TO P2")
            mahjong_game.goto_p1_end()
            r.set('game_state', mahjong_game.state)
    elif mahjong_game.state == "p1_end":
        if tiles1.count("1") == 2:
            # p1 needs to discard a tile by putting it face down
            mahjong_game.goto_p2_start()
            r.set('game_state', mahjong_game.state)
    elif mahjong_game.state == "p2_start":
        r.set('game_state', mahjong_game.state)
        if tiles2.count("1") == 3:
            # check for p2 tiles up
            # check win combi
            # once all up go to p2 end
            mahjong_game.goto_p2_end()
            r.set('game_state', mahjong_game.state)
    elif mahjong_game.state == "p2_end":
        r.set('game_state', mahjong_game.state)
        if tiles2.count("1") == 2:
            # p2 needs to discard a tile by putting it face down
            mahjong_game.goto_p1_start()
            r.set('game_state', mahjong_game.state)
    else:
        print "doesn't seem to be something p1_update needs to care about"
        sys.stdout.flush()


tiles = ['north', 'south', 'east', 'west', 'circle_1', 'circle_2', 'circle_3', 'circle_4', 'circle_5', 'circle_6', 'circle_7', 'circle_8', 'circle_9', 'number_1', 'number_2', 'number_3', 'number_4', 'number_5', 'number_6', 'number_7', 'number_8', 'number_9']


def send_a_tile_to_user(user):
    token = ""
    tiles = {}
    if user == "p1":
        tiles = jsonpickle.loads(r.get('user1_live_tiles'))
    if user == "p2":
        tiles = jsonpickle.loads(r.get('user2_live_tiles'))

    for key, value in tiles.iteritems():
        if value.orientation == "0":
            token = value.token
            break

    if token != "":
        listOfTiles = jsonpickle.loads(r.get('listOfTiles'))
        tile_to_send = listOfTiles.pop()
        app.logger.debug(str(tile_to_send))
        app.logger.debug(str(token))
        photon_call.construct_tile_async(tile=str(tile_to_send), token=token)
        r.set('listOfTiles', jsonpickle.dumps(listOfTiles))


class Mahjong(object):
    def send_p1_tile(self):
        #for user1 tile set send him a tile
        send_a_tile_to_user("p1")
        send_gcm_message("DRAW", gcm_bot.iot_mahjong_s6)
        send_gcm_message("WAIT", gcm_bot.iot_mahjong)

    def tell_p1_discard(self):

        send_gcm_message("DISCARD", gcm_bot.iot_mahjong_s6)
        send_gcm_message("WAIT", gcm_bot.iot_mahjong)

    def send_p2_tile(self):
        send_a_tile_to_user("p1")
        send_gcm_message("WAIT", gcm_bot.iot_mahjong_s6)
        send_gcm_message("DRAW", gcm_bot.iot_mahjong)

    def tell_p2_discard(self):
        send_gcm_message("WAIT", gcm_bot.iot_mahjong_s6)
        send_gcm_message("DISCARD", gcm_bot.iot_mahjong)

def start_the_game():
    print "GAME STARTED!"
    sys.stdout.flush()

    listOfTiles = randomTileGen(100)

    # assign tiles
    # send to photon
    reqList = []
    for i in range(3):
        photon_token = user1_tiles[i]
        tile_to_send = tiles.index(listOfTiles.pop())
        reqList.append(photon_call.construct_tile_async(tile=str(tile_to_send), token=photon_token))

    for i in range(3):
        photon_token = user2_tiles[i]
        tile_to_send = tiles.index(listOfTiles.pop())
        reqList.append(photon_call.construct_tile_async(tile=str(tile_to_send), token=photon_token))

    grequests.map(reqList)

    # store list of tiles in redis
    r.set('listOfTiles', jsonpickle.dumps(listOfTiles))

    # trigger source dest
    transitions = [
        # starting will expect both players to have tiles in a particular order
        { 'trigger': 'goto_p1_start', 'source': 'starting', 'dest': 'p1_start', 'before': 'send_p1_tile'},
        # send p1 tile and say please flip up your tiles
        { 'trigger': 'goto_p1_end', 'source': 'p1_start', 'dest': 'p1_end', 'before':'tell_p1_discard'},
        # say p1 now please discard a tile, flip 1 down
        { 'trigger': 'goto_p2_start', 'source': 'p1_end', 'dest': 'p2_start', 'before': 'send_p2_tile'},
        # send p2 tile and say please flip up your tiles
        { 'trigger': 'goto_p2_end', 'source': 'p2_start', 'dest': 'p2_end', 'before':'tell_p2_discard' },
        # say p2 now please discard a tile, flip 1 down
        { 'trigger': 'goto_p1_again', 'source': 'p2_end', 'dest': 'p1_start', 'before':'send_p1_tile' },
        # go back to 1 if nobody won
        { 'trigger': 'p1_wins', 'source': 'p1_start', 'dest': 'p1_winner' },
        { 'trigger': 'p2_wins', 'source': 'p2_start', 'dest': 'p2_winner' }
    ]

    # setup machine
    mahjong_game = Mahjong()
    machine = Machine(mahjong_game, states=['starting', 'p1_start', 'p1_end', 'p2_start', 'p2_end', 'p1_win', 'p2_win'], transitions=transitions, initial='starting')

    # set game state
    r.set('game_state', mahjong_game.state)


    print "SUBSCRIBED && MACHINE CREATED!", mahjong_game.state
    sys.stdout.flush()

    app.logger.debug(r.get('game_state'))


    #push notification tell p1 to arrange 2 up and 1 down
    #tell p2 to have all 3 up
    app.logger.debug("SEND P1 & P2 STARTING SETUP!")

    # s6 is p1 , s4 is p2
    send_gcm_message("SETUP_P1", gcm_bot.iot_mahjong_s6)
    send_gcm_message("SETUP_P2", gcm_bot.iot_mahjong)

# On android app, play game button should trigger this
@app.route('/joingame', methods=['POST', 'GET'])
def join_game():
    player = request.args.get('player', '')
    if len(player) <= 0:
        return "need a player to join"

    player_list = jsonpickle.loads(r.get('online_clients'))

    if len(player_list) >= 2:
        return "already started"

    if (player in player_list) == False:
        app.logger.debug("GAME :: TO BE STARTED")
        player_list.append(player)
        r.set('online_clients', jsonpickle.dumps(player_list))

    if len(player_list) >= 2:
        # pub.subscribe(p1_update, 'p1_update')
        # pub.subscribe(p2_update, 'p2_update')
        start_the_game()
        return "started"
    return "need another player"

# forcefully reset the game, should broadcast to all clients, reset whatever to clean state
@app.route('/resetgame', methods=['POST', 'GET'])
def reset_game():
    r.set('online_clients', jsonpickle.dumps([]))
    app.logger.debug("online_clients :: " + r.get('online_clients'))
    return "reset"

@app.route('/fakep1update', methods=['GET'])
def fire_p1_update():
    player_update("")
    return "meow"

@app.route('/fakep2update', methods=['GET'])
def fire_p2_update():
    mahjong_game.goto_p1_start()
    app.logger.debug(mahjong_game.state)
    return "chirpy chirp chirp"

@app.route('/forcestart', methods=['GET'])
def force_start_game():
    start_the_game()
    return "pew pew"

##################################################################
# PHOTON UPDATES
##################################################################

# Handles each tile's update and sets it in redis (triplets)
def tileUpdateHandler(tile_data):
    tiles1 = jsonpickle.loads(r.get('user1_live_tiles'))
    tiles2 = jsonpickle.loads(r.get('user2_live_tiles'))
    # app.logger.debug(jsonpickle.dumps(tiles1))
    if "source" in tile_data:
        if tile_data["source"] in user1_tiles:
            # if tiles1[tile_data["source"]].orientation != tile_data["orientation"]:
            #     #updates
            #     app.logger.debug('TILE1 CHANGE IN ORIENTATION')
            #     pub.sendMessage('p1_update', tiles=tiles1, extra=None)

            tiles1[tile_data["source"]].orientation = tile_data["orientation"]
            tiles1[tile_data["source"]].kind = tile_data["tile"] # update tile kind with "tile from photon"
            tiles1[tile_data["source"]].x = tile_data["x"]
            tiles1[tile_data["source"]].y = tile_data["y"]
            tiles1[tile_data["source"]].z = tile_data["z"]
            r.set('user1_live_tiles', jsonpickle.dumps(tiles1))



        elif tile_data["source"] in user2_tiles:
            # if tiles2[tile_data["source"]].orientation != tile_data["orientation"]:
            #     #updates
            #     app.logger.debug('TILE2 CHANGE IN ORIENTATION')
            #     pub.sendMessage('p2_update', tiles=tiles2, extra=None)

            tiles2[tile_data["source"]].orientation = tile_data["orientation"]
            tiles2[tile_data["source"]].kind = tile_data["tile"] # update tile kind with "tile from photon"
            tiles2[tile_data["source"]].x = tile_data["x"]
            tiles2[tile_data["source"]].y = tile_data["y"]
            tiles2[tile_data["source"]].z = tile_data["z"]
            r.set('user2_live_tiles', jsonpickle.dumps(tiles2))

        else:
            app.logger.debug('An error occurred processing tile data.')

@app.route('/photonUpdate', methods=['POST'])
def photonUpdate():
    content = request.get_json(silent=True, force=True)
    # remove the additional property particle servers provide
    content.pop("data", None)
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
    app.logger.debug(data)
    resp = Response(response=data,
    status=200, \
    mimetype="application/json")
    return resp

@app.route('/playermove', methods=['POST'])
def playermove():
    content = request.get_json(silent=True, force=True)
    player_update()
    app.logger.debug(content)
    return "player move"



##################################################################
# ROUTING
##################################################################
@app.route('/')
def main():
    # return "test"
    return render_template('./sparktemplate.html', tempdata=1, utimedata=1,
                           ledstatus=1, authbool=True)

##################################################################
# Example of how you would use the XMPP object to send message.
##################################################################
@app.route("/gcm")
def gcmTest():
    message = {
        "to": gcm_bot.iot_mahjong_s6,
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


if __name__ == '__main__':
    # TODO: add algo to make the tiles here
    app.run()
