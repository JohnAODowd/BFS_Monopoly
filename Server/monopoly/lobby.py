import monopoly.redisLib as r
from monopoly import helpers
from monopoly.getData import getInitJson, getFigurinesJson, getBoardJson, getPropertiesJson
"""
Library for host/join and general lobby functionality
"""

# Methods to write:
#   checkTime
#   forceStart

def _start(gID):
    # moves players to starting square on board
    players = r.getPlayers(gID)
    board 	= getBoardJson()
    for _uID in players:
        board[0]['playersOn'] += [players[_uID]['public']['number']]
    r.setBoard(gID, board)

def setInitProperties(gID):
    # gets the initial properties from JSON and organises them into a deeds layout
    properties = getPropertiesJson()
    newProp = {}
    for key in properties:
        newProp[key] = properties[key]
        if "rent" in properties[key]:
            if "colourGroup" in properties[key]:
                newProp[key]['group'] = properties[key]['colourGroup']
                newProp[key].pop('colourGroup', None)
                newProp[key]['groupSize'] = properties[key]['size']
                newProp[key].pop('size', None)
                newProp[key]['buildPrice'] = newProp[key]['house1']
                newProp[key]['buildings']    = 0

        elif "railroad" in key:
            newProp[key]['group'] = 'transport'
            newProp[key]['groupSize'] = properties[key]['size']
            newProp[key].pop('size', None)
        else:
            newProp[key]['group'] = 'services'
            newProp[key]['groupSize'] = properties[key]['size']
            newProp[key].pop('size', None)
        newProp[key]['status']       = 'notOwned'
        newProp[key]['pID']          = key
    r.setDeeds(gID, newProp)

def getPlayerPropertiesDict():
    # returns the dict structure for property storage in players
    groups = {
                "darkBlue":{
                    "owned":[],
                    "size":2
                },
                "yellow":{
                    "owned": [],
                    "size":3
                },
                "brown":{
                    "owned": [],
                    "size":2
                },
                "pink":{
                    "owned": [],
                    "size":3
                },
                "green":{
                    "owned": [],
                    "size":3
                },
                "red":{
                    "owned": [],
                    "size":3
                },
                "lightBlue":{
                    "owned": [],
                    "size":3
                },
                "orange":{
                    "owned": [],
                    "size":3
                },
                "transport" : {
                    "owned": [],
                    "size":4
                },
                "services" : {
                    "owned": [],
                    "size":2
                }
            }

    return groups

def getFigurinesList():
    # returns a list of figurines
    figurines = getFigurinesJson()
    lst = []
    for key in figurines:
        lst += [key]
    return lst

def isHost(gID, uID):
    player = r.getPlayers(gID)[uID]
    return player['public']['number'] == 1

def canStart(gID, uID):                         #checks to see if starting is a viable option
    game = r.getGame(gID)
    players = r.getPlayers(gID)
    if players[uID]['public']['number'] == 1:
        if game['playersNo'] > 1:
            if game['playersNo'] == 8 - len(game['figurines']):
                return True
    return False

def host(json):
    #sets a game + host player
    try:
        game                    = {}
        gID                     = helpers.genID()
        game['gID']             = gID
        game['GO']              = getInitJson()['go']
        game['type']            = json['type']
        game['playersNo']       = 0
        game['turn']            = 1
        game['lastActivity']    = helpers.getTime()
        game['figurines']       = getFigurinesList()
        game['state']           = 'LOBBY'
        game["lastRoll"]        = {}
        game['takenGOOJF']      = {"CommunityChest" : False, "Chance" : False}
        game['buildings']       = getInitJson()['buildings']
        game['trade']           = {}
        r.setGame(gID, game)

        r.init(gID)

        setInitProperties(gID)
        ret         = join(json, gID)
        return ret
    except:
        ret             = {}
        ret['error']    = 'host'
        return ret

def join(json, gID=None):
    #sets a player
    ret = {}
    if gID == None:
        if "gID" in json:
            gID                                         = json['gID']
        else:
            gID                                         = helpers.getfirstPublicGame()
    try:
        game                                            = r.getGame(gID)
        if game['playersNo'] == 8:
            ret['error']                                = 'Game is full. Try again.'
        else:
            game['playersNo']                           += 1
            uID                                         = helpers.genID()
            player                                      = {}
            player['uID']                               = uID
            player['money']                             = getInitJson()['startMoney']
            player['options']                           = []
            player["trade"]                             = {}
            player["trade"]["sent"]                     = {}
            player["trade"]["recieved"]                 = []
            player['public']                            = {}
            player['public']['name']                    = json['name']
            player['public']['number']                  = game['playersNo']
            player['public']['properties']              = getPlayerPropertiesDict()
            player['public']['GOOJF']                   = {"CommunityChest" : False, "Chance" : False, }
            player['public']['position']                = 0
            player['public']['figurine']                = None
            player['public']['jail']                    = {}
            player['public']['jail']['boolean']         = False
            player['public']['jail']['turn']            = 0
            player["canBuy"]                            = None

            r.setPlayer(gID, uID, player)
            r.setGame(gID, game)
            ret = helpers.getReturnData(gID, uID, ["FIGURINE"])

    except:
        ret['error'] = 'join'
    return ret

def selectFigurine(json):
    #used in lobby to select players figurine
    game    = r.getGames()[json['gID']]

    if json['figurine'] in game['figurines']:

        player                          = r.getPlayers(json['gID'])[json['uID']]
        player['public']['figurine']    = json['figurine']

        game['figurines'].remove(json['figurine'])
        r.setPlayer(json['gID'], json['uID'], player)
        r.setGame(json['gID'], game)

        ret = helpers.getReturnData(json['gID'], json['uID'], [], ["FIGURINE"])
    else:
        ret = {}
        ret['error']        = 'figurine'
    return ret

def ping(json):
    gID             = json['gID']
    uID             = json['uID']
    if isHost(gID, uID):
        if canStart(gID, uID):
            ret = helpers.getReturnData(gID, uID, ["START"])
        else:
            ret = helpers.getReturnData(gID, uID, [], ["START"])
    else:
        ret = helpers.getReturnData(gID, uID)
    return ret

def start(json):
    #initialises the board and starts the game
    gID = json['gID']
    uID = json['uID']
    if canStart(gID, uID):
        game            = r.getGame(gID)
        game['state']   = "PLAYING"
        r.setGame(gID, game)
        _start(gID)

        players        = r.getPlayers(gID)      #add the default options for the PLAYING state to all players
        for _uID in players:
            players[_uID]["options"].append("TRADE")
            players[_uID]["options"].append("MORTGAGE")
        r.setPlayers(gID, players)

        ret = helpers.getReturnData(gID, uID, ["ROLL"], ["START"])
    else:
        ret = {}
        ret['error'] = "START"
    return ret

def lobby(json):
    ret = {"'error':'lobby'"}
    if 'gID' in json and 'uID' in json:                                 # if user has valid uID and gID
        if r.validateUID(json['gID'], json['uID']):

            if json['request'] == 'FIGURINE':                           # user selecting figurine
                ret = selectFigurine(json)
            elif json['request'] == 'PING':                             # user polling for details
                ret = ping(json)
            elif json['request'] == "START":
                ret = start(json)
        
    elif json["request"] == "JOIN":                                     # set join user details
        ret = join(json)
    elif json['request'] == 'HOST':                                   # set host user details
            ret = host(json)

    return ret