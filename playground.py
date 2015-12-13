from mahjong_stm_objects import *
from mahjong_stm_util import *
import json, jsonpickle
import redis
import os
# r = redis.from_url(os.environ.get("HEROKU_REDIS_MAUVE_URL"))

# orange
user1_tiles = ["250040000347343337373737", "2b002d000447343233323032", "3b003d000347343339373536"]
# green
user2_tiles = ["210039000347343337373737", "1c003e000d47343432313031", "37001c001347343432313031"]

temp_user_tiles1 = {}
temp_user_tiles2 = {}

for token in user1_tiles:
    temp_user_tiles1[token] = Tile(token=token)

for token in user2_tiles:
    temp_user_tiles2[token] = Tile(token=token)


def tileUpdateHandler(tile_data):
    # tiles1 = jsonpickle.loads(r.get('user1_live_tiles'))
    # tiles2 = jsonpickle.loads(r.get('user2_live_tiles'))
    tiles1 = temp_user_tiles1
    tiles2 = temp_user_tiles2
    print "hello"
    if "source" in tile_data:
        print "source"
        print tile_data["source"]
        if tile_data["source"] in user1_tiles:
            print "meow"
            tiles1[tile_data["source"]].orientation = tile_data["orientation"]
            tiles1[tile_data["source"]].kind = tile_data["tile"] # update tile kind with "tile from photon"
            tiles1[tile_data["source"]].x = tile_data["x"]
            tiles1[tile_data["source"]].y = tile_data["y"]
            tiles1[tile_data["source"]].z = tile_data["z"]
            # r.set('user1_live_tiles', jsonpickle.dumps(tiles1))
            print tile_data1["orientation"]
            if tiles1[tile_data["source"]].orientation != tile_data["orientation"]:
                #updates
                pass

        elif tile_data["source"] in user2_tiles:
            print "is tile2"
            tiles2[tile_data["source"]].orientation = tile_data["orientation"]
            tiles2[tile_data["source"]].kind = tile_data["tile"] # update tile kind with "tile from photon"
            tiles2[tile_data["source"]].x = tile_data["x"]
            tiles2[tile_data["source"]].y = tile_data["y"]
            tiles2[tile_data["source"]].z = tile_data["z"]
            # r.set('user2_live_tiles', jsonpickle.dumps(tiles2))
            if tiles2[tile_data["source"]].orientation != tile_data["orientation"]:
                #updates
                pass
        else:
            print "error occurred while processing tile data"

atile = {'orientation': '0', 'tile': '0', 'timestamp': '3179788', 'coreid': '210039000347343337373737', 'source': '210039000347343337373737', 'published_at': '2015-12-12T14:44:02.711Z', 'event': 'custom_pblish_event_dev', 'y': '1901.000000', 'x': '1933.000000', 'z': '792.000000'}

tileUpdateHandler(atile)