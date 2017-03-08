import redis
from json import dumps, loads

r = redis.StrictRedis(host='redis.netsoc.co', port=6379, db=0)

"""
Used for setting and getting data from redis database
"""

def keyStringtoInt(dictionary):
    # convert all top level dict string keys to ints
    # eg {"0":"abc} -> {0:"abc"}
    return {int(k):v for k,v in dictionary.items()}

def getGames():  # gets all games in redis
    return loads(r.get('games').decode("utf-8"))

def init(gID):
    r.set('players of ' + gID, "{}")
    r.set('board of ' + gID, "{}")
    r.set('deeds of ' + gID, "{}")
    r.set('chat of ' + gID, "{}")

def getGame(gID):  # gets a specific game with gID
    games = getGames()
    game = games[gID]
    return game

def getPlayers(gID):  # gets all players for a game with gID
    return loads(r.get('players of ' + gID).decode("utf-8"))

def getBoard(gID):  # returns the board for a game using gID
    return keyStringtoInt(loads(r.get('board of ' + gID).decode("utf-8")))

def getDeeds(gID):
    return loads(r.get('deeds of ' + gID).decode("utf-8"))

def getChat(gID):
    return loads(r.get('chat of ' + gID).decode("utf-8"))

def setGame(gID, game):  # sets a game in redis; gID <String> + game <dict>
    games       = getGames()
    games[gID]  = game
    r.set('games', dumps(games).encode("utf-8"))

def setPlayers(gID, players):
    r.set('players of ' + gID, dumps(players).encode("utf-8"))

def setPlayer(gID, uID, player):  # sets a player, takes gID + uID + player <dict>
    players = getPlayers(gID)
    players[uID] = player
    r.set('players of ' + gID, dumps(players).encode("utf-8"))

def setBoard(gID, board):
    r.set('board of ' + gID, dumps(board).encode("utf-8"))
    return board

def setDeeds(gID, deeds):
    r.set('deeds of ' + gID, dumps(deeds).encode("utf-8"))

def setDeed(gID, pID, deed):
    deeds       = getDeeds(gID)
    deeds[pID]  = deed
    setDeeds(gID, deeds)


def setChat(gID, chat):
    r.set('chat of ' + gID, dumps(chat).encode("utf-8"))

def validateGID(gID):  # used to validate a gID
    games = getGames()
    if gID in games:
        return True
    else:
        return False

def validateUID(gID, uID):  # used to validate a uID
    players = getPlayers(gID)
    if uID in players:
        return True
    else:
        return False