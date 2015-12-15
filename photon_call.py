import requests
import sys
import grequests

# file called credentials.py which constains the following vars
from credentials import *

# PARTICLE_ID="YOUR_PARTICLE_ID"
# PARTICLE_ACCESS_TOKEN="YOUR_ACCESS_TOKEN"
# PARTICLE_FUNCTION = "YOUR_PARTICLE_FUNCTION"
def callback_function(response):
  # response.code # The HTTP status code
  # response.headers # The HTTP headers
  # response.body # The parsed response
  # response.raw_body # The unparsed response
  print response.code
  sys.stdout.flush()

def get_data_async(tile=None, token=None):
    print "contructing"
    sys.stdout.flush()
    if (tile == None):
        tile = 0

    PARTICLE_FUNCTION = "getdata"
    URL = "https://api.particle.io/v1/devices/"
    SLASH = "/"
    TOKEN_LABEL = "?access_token="
    PAYLOAD = {"args": tile}
    return grequests.get(URL + token + SLASH +
                           PARTICLE_FUNCTION + TOKEN_LABEL +
                           PARTICLE_ACCESS_TOKEN)

def construct_tile_async(tile=None, token=None):
    print "contructing"
    sys.stdout.flush()
    if (tile == None):
        tile = 0

    PARTICLE_FUNCTION = "tile"
    URL = "https://api.particle.io/v1/devices/"
    SLASH = "/"
    TOKEN_LABEL = "?access_token="
    PAYLOAD = {"args": tile}
    return grequests.post(URL + token + SLASH +
                           PARTICLE_FUNCTION + TOKEN_LABEL +
                           PARTICLE_ACCESS_TOKEN, json=PAYLOAD)

def send_tile(tile=None, token=None):
    # VARIABLES

    if (tile == None):
        tile = 0

    PARTICLE_FUNCTION = "tile"
    URL = "https://api.particle.io/v1/devices/"
    SLASH = "/"
    TOKEN_LABEL = "?access_token="
    PAYLOAD = {"args": tile}

    # COMMANDLINE ARGS
    # 0 -  file_name.py , 1 - arg[0] ...
    # if (len(sys.argv) > 1):
    #     PAYLOAD = {"args": sys.argv[1]}

    # MAGIC
    print "Dancing monkeys are executing your request..."
    result = requests.post(URL + token + SLASH +
                           PARTICLE_FUNCTION + TOKEN_LABEL +
                           PARTICLE_ACCESS_TOKEN, json=PAYLOAD)
    return result.text


def sendToPhoton(payload_for_sending=None):
    # VARIABLES

    if (payload_for_sending == ""):
        payload_for_sending = "0"

    PARTICLE_FUNCTION = "tile"
    URL = "https://api.particle.io/v1/devices/"
    SLASH = "/"
    TOKEN_LABEL = "?access_token="
    PAYLOAD = {"args": payload_for_sending}

    # COMMANDLINE ARGS
    # 0 -  file_name.py , 1 - arg[0] ...
    if (len(sys.argv) > 1):
        PAYLOAD = {"args": sys.argv[1]}

    # MAGIC
    print "Dancing monkeys are executing your request..."
    result = requests.post(URL + PARTICLE_ID + SLASH +
                           PARTICLE_FUNCTION + TOKEN_LABEL +
                           PARTICLE_ACCESS_TOKEN, json=PAYLOAD)
    return result.text

def getFromPhoton(pid=None):
    print "getting from photon!"
    if pid == None:
        pid = PARTICLE_ID

    PARTICLE_FUNCTION = "getpos"
    URL = "https://api.particle.io/v1/devices/"
    SLASH = "/"
    TOKEN_LABEL = "?access_token="
    result = requests.get(URL + pid + SLASH +
                            PARTICLE_FUNCTION + TOKEN_LABEL + PARTICLE_ACCESS_TOKEN)

    print result.text
    return result.text

if __name__ == "__main__":
    send_tile_async(tile="0", token="2b002d000447343233323032")
