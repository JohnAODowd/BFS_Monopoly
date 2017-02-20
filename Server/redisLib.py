import redis
from json import dumps, loads
from monopolyVars import getInitBoard

# TODO create monopolyVars
# TODO unit test

r = redis.StrictRedis(host='localhost', port=6379, db=0)

"""
Used for setting and getting data from redis database
"""

def getGames():															#gets all games in redis
	return loads(r.get('Games').decode("utf-8"))

def getGame(gID):														#gets a specific game with gID
	games 	= getGames()
	game 	= games[gID]
	return game

def getPlayers(gID):													#gets all players for a game with gID
	return loads(r.get('players of ' + gID).decode("utf-8"))

def getPlayer(gID, uID):												#gets specific player using gID and uID
	players = getPlayers(gID)
	player 	= players[uID]
	return player

def getBoard(gID):														#returns the board for a gamee using gID
	return loads(r.get('board of ' + gID).decode("utf-8"))

def getSquare(gID, squareNo):											#returns a board square using gID and squareNo
	return getBoard(gID)[squareNo]

def setPlayer(gID, uID, player):										#sets a player, takes gID + uID + player <dict>
	players 		= getPlayers(gID)
	players[uID]	= player
	r.set('players of ' + gID, dumps(player).encode("utf-8"))

def setBoard(gID):														#sets a board, takes gID + board <dict>
	board 				= getInitBoard()
	players 			= getPlayers(gID)
	for player in players:
		board[player['public']['position']]["playersOn"] = player['name']
	r.set('board of ' + gID, dumps(board).encode("utf-8"))
	return board

def setSquare(gID, squareNo, square):									#sets a square, takes gID + squareNo + square<dict>
	board 			= getBoard()
	board[squareNo] = square
	r.set('board of ' + gID, dumps(board).encode("utf-8"))

def validateGID(gID):													#used to validate a gID
	games = getGames()
	return gID in games

def validateUID(gID, uID):												#used to validate a uID
	players = getPlayers(gID)
	return uID in players