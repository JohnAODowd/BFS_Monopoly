import random
import string
from _sha256 import sha256
from datetime import datetime
from monopoly import redisLib as r


def getTime():                                                          #used for updating  activity time
    now = datetime.now()
    return str(now.strftime("%Y-%m-%d %H:%M:%S"))

def genString(size=10, chars=string.ascii_uppercase + string.digits):   #used for generating IDs
	return ''.join(random.choice(chars) for _ in range(size))

def genID():
	token = sha256(genString().encode('utf-8')).hexdigest()             #generates ID's
	return token

def getfirstPublicGame():                                               #used to connect to random public game
    games   = r.getGames()
    for gID in games:
        if games[gID]["type"] == "public" and games[gID]["playersNo"] < 8:
            return gID
    return False
