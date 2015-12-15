from gcm import GCM

def send_gcm_message(message, reg_id):
    gcm = GCM("AIzaSyAf6J6MHvUlpnT_FIOoCws8Fs8oL7E0oOc")
    data = {'message': message}
    gcm.plaintext_request(registration_id=reg_id, data=data)

send_gcm_message("WAIT", "c198uVK7Dgw:APA91bEvUwogy4q0Px33WfHpOPvOZe6U7uCML1hd1e7LDuBfoGC7zdErxWvBpld-FczRi8hFc4z5brY-WEIXXsXFiAgTQ9Ligyk_acrMfClitaq9mzyNqgW8RB2r76Tz8FjCZVYJbEhF")

# # Plaintext request
# reg_id = '12'
# gcm.plaintext_request(registration_id=reg_id, data=data)

# # JSON request
# reg_ids = ['12', '34', '69']
# response = gcm.json_request(registration_ids=reg_ids, data=data)

# # Extra arguments
# res = gcm.json_request(
#     registration_ids=reg_ids, data=data,
#     collapse_key='uptoyou', delay_while_idle=True, time_to_live=3600
# )

# # Topic Messaging
# topic = 'foo'
# gcm.send_topic_message(topic=topic, data=data)
#

# from transitions import Machine

# class Matter(object):
#     def __init__(self): self.set_environment()
#     def set_environment(self, temp=0, pressure=101.325):
#         self.temp = temp
#         self.pressure = pressure
#     def print_temperature(self): print("Current temperature is %d degrees celsius." % self.temp)
#     def print_pressure(self): print("Current pressure is %.2f kPa." % self.pressure)

# lump = Matter()
# machine = Machine(lump, ['solid', 'liquid'], initial='solid')
# machine.add_transition('melt', 'solid', 'liquid', before='set_environment')

# lump.melt(45)  # positional arg
# lump.print_temperature()
# print lump.state
# # print lump.print_temperature()
# machine.set_state('solid')  # reset state so we can melt again
# lump.melt(pressure=300.23)  # keyword args also work
# lump.print_pressure()
# machine.set_state('liquid')
# print lump.state

# import json
# import jsonpickle
# from mahjong_stm_objects import *
# from mahjong_stm_util import *


# # complete tile list
# tiles = ['north', 'south', 'east', 'west', 'circle_1', 'circle_2', 'circle_3',
#          'circle_4', 'circle_5', 'circle_6', 'circle_7', 'circle_8',
#          'circle_9', 'number_1', 'number_2', 'number_3', 'number_4',
#          'number_5', 'number_6', 'number_7', 'number_8', 'number_9']

# def check_if_win(tile_dict):
#     hasWon = False

#     current_combinations = []

#     for key, value in tile_dict.iteritems():
#         # value kind should be a string
#         current_combinations.append(value["kind"])

#     try:
#         current_combinations = [int(val) for val in current_combinations]
#         # map to names
#         current_combinations = [tiles[num] for num in current_combinations]
#     except:
#         app.logger.debug("Error converting string to int in current_combinations")

#     if current_combinations in winningCombinations:
#         print "you win"
#         hasWon = True

#     return hasWon


# fakedict = {"250040000347343337373737":
#             {"py/object": "mahjong_stm_objects.Tile",
#              "kind": "20",
#              "last_updated": None,
#              "orientation": "0",
#              "y": "2145.000000",
#              "x": "1756.000000",
#              "z": "2594.000000",
#              "token": "250040000347343337373737"},
#             "2b002d000447343233323032":
#             {"py/object": "mahjong_stm_objects.Tile",
#              "kind": "15",
#              "last_updated": None,
#              "orientation": "1",
#              "y": "1208.000000",
#              "x": "1033.000000",
#              "z": "1484.000000",
#              "token": "2b002d000447343233323032"},
#             "3b003d000347343339373536":
#             {"py/object": "mahjong_stm_objects.Tile",
#              "kind": "6",
#              "last_updated": None,
#              "orientation": "1",
#              "y": "2259.000000",
#              "x": "1017.000000",
#              "z": "1517.000000",
#              "token": "3b003d000347343339373536"}}

# fakedict_win = {"250040000347343337373737":
#             {"py/object": "mahjong_stm_objects.Tile",
#              "kind": "15",
#              "last_updated": None,
#              "orientation": "0",
#              "y": "2145.000000",
#              "x": "1756.000000",
#              "z": "2594.000000",
#              "token": "250040000347343337373737"},
#             "2b002d000447343233323032":
#             {"py/object": "mahjong_stm_objects.Tile",
#              "kind": "15",
#              "last_updated": None,
#              "orientation": "1",
#              "y": "1208.000000",
#              "x": "1033.000000",
#              "z": "1484.000000",
#              "token": "2b002d000447343233323032"},
#             "3b003d000347343339373536":
#             {"py/object": "mahjong_stm_objects.Tile",
#              "kind": "15",
#              "last_updated": None,
#              "orientation": "15",
#              "y": "2259.000000",
#              "x": "1017.000000",
#              "z": "1517.000000",
#              "token": "3b003d000347343339373536"}}


# print check_if_win(fakedict) # False
# print check_if_win(fakedict_win) # True