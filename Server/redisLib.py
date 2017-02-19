from hashlib import sha256
import redis
import random
import string
from json import dumps, loads
from monopolyVars import getInitBoard

# TODO create monopolyVars
# TODO unit test

r = redis.StrictRedis(host='localhost', port=6379, db=0)

def genString(size=10, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def genID():
	token = sha256(genString().encode('utf-8')).hexdigest()
	return token

def getGames():
	return loads(r.get('Games').decode("utf-8"))

def getGame(gID):
	games 	= getGames()
	game 	= games[gID]
	return game

def getPlayers(gID):
	return loads(r.get('players of ' + gID).decode("utf-8"))

def getPlayer(gID, uID):
	players = getPlayers(gID)
	player 	= players[uID]
	return player

def getBoard(gID):
	return loads(r.get('board of ' + gID).decode("utf-8"))

def getSquare(gID, squareNo):
	return getBoard(gID)[squareNo]

def setGame(game):
	pass

def setPlayer(gID, uID, player):
	players 		= getPlayers(gID)
	players[uID]	= player
	r.set('players of ' + gID, dumps(player).encode("utf-8"))

def setBoard(gID):
	board 					= getInitBoard()
	players 				= getPlayers(gID)
	publicPlayers			= {}
	for player in players:
		publicPlayers[player["public"]["number"]] = player["public"]
	board[0]["playersOn"] 	= publicPlayers
	r.set('board of ' + gID, dumps(board).encode("utf-8"))
	
def setSquare(gID, squareNo, square):
	board 			= getBoard()
	board[squareNo] = square
	r.set('board of ' + gID, dumps(board).encode("utf-8"))

