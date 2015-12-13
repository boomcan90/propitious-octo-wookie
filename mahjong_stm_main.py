from mahjong_stm_objects import *
from mahjong_stm_util import *
import time
import redis
import sys, os
from pubsub import pub
from transitions import Machine

redis_url = os.getenv('HEROKU_REDIS_MAUVE_URL', 'redis://localhost:6379')
r = redis.from_url(redis_url)

# orange: pirate, morphing, zombie
user1_tiles = ["250040000347343337373737", "2b002d000447343233323032", "3b003d000347343339373536"]
# green: raptor, hunter, dentist
user2_tiles = ["210039000347343337373737", "1c003e000d47343432313031", "37001c001347343432313031"]

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

def p1_update(tiles, extra=None):
    tiles1 = jsonpickle.loads(r.get('user1_live_tiles'))
    tiles2 = jsonpickle.loads(r.get('user2_live_tiles'))
    # tiles1 = parseTileOrientation(tiles1)
    # tiles2 = parseTileOrientation(tiles2)

    print "p1 update received!"
    sys.stdout.flush()
    print tiles1
    sys.stdout.flush()

    if machine.state == "starting":
        if tiles1.count(1) == 2 and tiles2.count == 3:
            # check for both p1 and p2
            # then got goto p1
            machine.goto_p1_start()
    elif machine.state == "p1_start":
        if tiles1.count(1) == 3:
            # check for p1 tiles up
            # check win combi
            # once all up go to p1 end
            machine.goto_p1_end()
    elif machine.state == "p1_end":
        if tiles1.count(1) == 2:
            # p1 needs to discard a tile by putting it face down
            machine.goto_p2_start()
    else:
        print "doesn't seem to be something p1_update needs to care about"
        sys.stdout.flush()


def p2_update(tiles, extra=None):
    tiles1 = jsonpickle.loads(r.get('user1_live_tiles'))
    tiles2 = jsonpickle.loads(r.get('user2_live_tiles'))
    tiles1 = parseTileOrientation(tiles1)
    tiles2 = parseTileOrientation(tiles2)

    print "p2 update received!"
    sys.stdout.flush()
    print tiles2
    sys.stdout.flush()

    if machine.state == "starting":
        # check for both p1 and p2 starts
        if tiles1.count(1) == 2 and tiles2.count == 3:
            machine.goto_p1_start()
    elif machine.state == "p2_start":
        if tiles2.count(1) == 3:
            # check for p2 tiles up
            # check win combi
            # once all up go to p2 end
            machine.goto_p2_end()
    elif machine.state == "p2_end":
        if tiles2.count(1) == 2:
            # p2 needs to discard a tile by putting it face down
            machine.goto_p1_start()
    else:
        print "doesn't seem to be something p2_update needs to care about"
        sys.stdout.flush()

class Mahjong(object):
    pass


def start_the_game():
    global machine
    global localWinningCombinations
    localWinningCombinations = winningCombinations[:]

    print "GAME STARTED!"
    sys.stdout.flush()

    global listOfTiles
    listOfTiles = randomTileGen(100)

    # assign tiles
    # send to photon


    # setup machine
    mahjong_game = Mahjong()
    machine = Machine(model=mahjong_game, states=['starting', 'p1_start', 'p1_end', 'p2_start', 'p2_end', 'p1_win', 'p2_win'], initial='starting')

    pub.subscribe(p1_update, 'p1_update')
    pub.subscribe(p2_update, 'p2_update')

    # trigger source dest
    transitions = [
        { 'trigger': 'goto_p1_start', 'source': 'starting', 'dest': 'p1_start' },
        { 'trigger': 'goto_p1_end', 'source': 'p1_start', 'dest': 'p1_end' },
        { 'trigger': 'goto_p2_start', 'source': 'p1_end', 'dest': 'p2_start' },
        { 'trigger': 'goto_p2_end', 'source': 'p2_start', 'dest': 'p2_end' },
        { 'trigger': 'goto_p1_again', 'source': 'p2_end', 'dest': 'p1_start' },
        { 'trigger': 'p1_wins', 'source': 'p1_start', 'dest': 'p1_winner' },
        { 'trigger': 'p2_wins', 'source': 'p2_start', 'dest': 'p2_winner' }
    ]

    print "SUBSCRIBED && MACHINE CREATED!"
    sys.stdout.flush()


if __name__ == "__main__":
    start_the_game()
