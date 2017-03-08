import random
import string
from _sha256 import sha256
from datetime import datetime, timedelta
from monopoly import redisLib as r

def getGameState(gID):
    return r.getGame(gID)['state']

def keyStringtoInt(dictionary):
    # convert all top level dict string keys to ints
    # eg {"0":"abc} -> {0:"abc"}
    return {int(k):v for k,v in dictionary.items()}

def getReturnData(gID, uID, optionsToAdd=[], optionsToRemove=[], alert={}, card=False):
    ret = {}
    game = r.getGame(gID)
    players = r.getPlayers(gID)
    player = players[uID]

    ret['players'] = {}
    for _uID in players:
        ret['players'][players[_uID]['public']['name']] = players[_uID]['public']

    if game['state'] != "LOBBY":
        ret['board'] = r.getBoard(gID)
        ret['deeds'] = r.getDeeds(gID)

        ret["chat"] = r.getChat(gID)

        ret["trade"] = {}
        if len(player["trade"]["recieved"]) > 0:
            ret["trade"]["recieved"] = player["trade"]["recieved"][0]

        if len(player["trade"]["sent"]) > 0:
            for tID in player["trade"]["sent"]:
                if player["trade"]["sent"][tID] == "declined":
                    game["trade"].pop(tID, None)
                    ret["trade"]["sent"] = player["trade"]["sent"][tID]["declined"] + "declined your trade offer"
                    player["trade"]["sent"].pop(tID, None)
                    r.setPlayer(gID, uID, player)
                    r.setGame(gID, game)
                    break
                if player["trade"]["sent"][tID] == "accepted":
                    game["trade"].pop(tID, None)
                    ret["trade"]["sent"] = player["trade"]["sent"][tID]["accepted"] + "accepted your trade offer"
                    player["trade"]["sent"].pop(tID, None)
                    r.setPlayer(gID, uID, player)
                    r.setGame(gID, game)
                    break

    if len(optionsToAdd) + len(optionsToRemove) > 0:
        for option in optionsToAdd:
            if option not in player['options']:
                player['options'] += [option]
        for option in optionsToRemove:
            try:
                if option == "BUY":
                    player["canBuy"] = None
                player['options'].remove(option)
            except:
                pass
        r.setPlayer(gID, uID, player)

    ret['options'] = player['options']
    if len(alert) != 0:
        ret['alert'] = alert
    if card:
        ret['card'] = card

    ret['game'] = game
    ret['player'] = player
    if game['state'] != "LOBBY" and (game["turn"] == player["public"]["number"]):
        print ("Return Data")
        print("name: " + player["public"]["name"])
        print("turn: " + str(game["turn"]))
        print("options: " + str(ret['options']))
        if "card" in ret:
            print (card['type'])
        if 'alert' in ret:
            print (alert)
        print("")
    return ret

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

def checkTime(lastActivity, limit, seconds=False):
    if seconds:
        limit       = timedelta(seconds=limit)
    else:
        limit       = timedelta(minutes=limit)
    now             = datetime.now()
    lActivity   = datetime.strptime(lastActivity, '%Y-%m-%d %H:%M:%S')
    return now <= lActivity + limit

def formToJson(form):
    json    = {}
    for key in form:
        if key == "private":
            json["type"] = "private"
        else:
            json[key]   = form[key]
    if "type" not in json and json['request'] == "HOST":
        json["type"] = "public"
    return json