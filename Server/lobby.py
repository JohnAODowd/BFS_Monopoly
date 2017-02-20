import random
import string
from _sha256 import sha256
import redisLib as r
from datetime import datetime
from monopolyVars import getFigurines

"""
Library for host/join and general lobby functionality
"""

#Helper Functions*******************************************************************
# TODO Test
# TODO move to their own file

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

#***********************************************************************************

def host(json):                                                         #sets a game + host player
    try:
        game                    = {}
        gID                     = genID()
        game['gID']             = gID
        game['type']            = json['type']
        game['playersNo']       = 0
        game['turn']            = 1
        game['lastActivity']    = getTime()
        game['figurines']       = getFigurines()
        game['status']          = 'LOBBY'
        r.setGame(gID, game)

        ret         = join(json, gID)
        return ret
    except:
        ret             = {}
        ret['error']    = 'host'
        return ret

def join(json, gID=None):                                                   #sets a player
    ret = {}
    if gID == None:
        gID                             = json['gID']
    try:
        game                            = r.getGames()[gID]
        if game['playerNo'] == 8:
            ret['error']                = 'full'
        else:
            game['playerNo']                += 1
            uID                             = genID()
            player                          = {}
            player['uID']                   = uID
            player['money']                 = 10000  # TODO fix
            player['public']                = {}
            player['public']['name']        = json['name']
            player['public']['number']      = game['playerNo']
            player['public']['properties']  = {}
            player['public']['GOOJF']       = 0
            r.setPlayer(gID, uID, player)
            r.setGame(gID, game)
            ret['player']                   = player
            ret['game']                     = game
    except:
        ret['error']                    = 'join'
    return ret

def selectFigurine(json):                                                   #used in lobby to select players figurine
    ret                     = {}
    game                    = r.getGames()[json['gID']]
    if json['figurine'] in game['figurines']:
        player              = r.getPlayer(json['gID'], json['uID'])
        player['figurine']  = json['figurine']
        game['figurines'].pop(json['figurine'])
        r.setPlayer(json['gID'], json['uID'], player)
        r.setGame(json['gID'], game)
        ret['player']       = player
        ret['game']         = game
    else:
        ret['error']        = 'figurine'
    return ret


