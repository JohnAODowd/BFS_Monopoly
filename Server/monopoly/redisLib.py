import redis
from json import dumps, loads
from monopoly.monopolyVars import getInitBoard, getInitBank
r = redis.StrictRedis(host='localhost', port=6379, db=0, password="Glad0s7334")

"""
Used for setting and getting data from redis database
"""

def getGames():  # gets all games in redis
    return loads(r.get('games').decode("utf-8"))

def getGame(gID):  # gets a specific game with gID
    games = getGames()
    game = games[gID]
    return game

def getPlayers(gID):  # gets all players for a game with gID
    return loads(r.get('players of ' + gID).decode("utf-8"))

def getPlayer(gID, uID):  # gets specific player using gID and uID
    players = getPlayers(gID)
    player = players[uID]
    return player

def getBoard(gID):  # returns the board for a game using gID
    return loads(r.get('board of ' + gID).decode("utf-8"))

def getBank(gID):
	return loads(r.get('bank of ' + gID).decode("utf-8"))

def setGame(gID, game):  # sets a game in redis; gID <String> + game <dict>
    games = getGames()
    games[gID] = game
    r.set('games', dumps(games).encode("utf-8"))

def setBank(gID, bank):
    r.set('bank of ' + gID, dumps(bank).encode("utf-8"))

def init(gID):
	r.set('players of ' + gID, "{}")
	r.set('board of ' + gID, "{}")
	r.set('bank of ' + gID, "{}")

def start(gID):
	players = getPlayers(gID)
	board 	= getInitBoard()
	bank 	= getInitBank()
	for player in players:
		board[0]['playersOn'] += [player['public']['number']]
	setBoard(gID, board)
	setBank(gID, bank)

def setPlayer(gID, uID, player):  # sets a player, takes gID + uID + player <dict>
    players = getPlayers(gID)
    players[uID] = player
    r.set('players of ' + gID, dumps(players).encode("utf-8"))

def setBoard(gID, board):
    r.set('board of ' + gID, dumps(board).encode("utf-8"))
    return board

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