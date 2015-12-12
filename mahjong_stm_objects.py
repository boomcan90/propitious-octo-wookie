import json

'''
Tile class:
Has attributes:
1. orientation- up or down
2. kind - which tile it is. (Command Line reference. haha.)
'''


class Tile:

    def __init__(self, orientation=None, x=None, y=None, z=None, kind=None, last_updated=None, token=None):
        self.orientation = orientation
        self.kind = kind
        self.token = token
        self.x = x
        self.y = y
        self.z = z
        self.last_updated = last_updated
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

    def __repr__(self):
        return json.dumps(self.__dict__)
###################################################################################################################################

'''
TODO:
1. Game states: create a state transition flow.
2. How to talk via GCM to android app.
3. Sending info to spark server.
(2 and 3 ==> integrate in flask code.)
4. isOnline is a redundant function.
    Need to create functions to do things when
    a particular command is recieved.
5. Do we want a points thing for user?
   Every time user wins, increase points by something?
   (Very simple, just add it to init.)

'''

class User:

    def __init__(self, username, onlineStatus=False, tiles=None, gameStatus='notPlaying', winning=None, turnStatus = None):
        self.username = username
        self.status = onlineStatus
        self.tiles = tiles
        self.gameStatus = gameStatus
        self.winning = winning
        self.turnStatus = turnStatus


###################################################################################################################################




