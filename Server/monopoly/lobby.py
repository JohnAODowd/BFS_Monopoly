import monopoly.redisLib as r
from monopoly.monopolyVars import getFigurines
from monopoly import helpers as help

"""
Library for host/join and general lobby functionality
"""

# TODO start
def host(json):                                                         #sets a game + host player
    try:
        game                    = {}
        gID                     = help.genID()
        game['gID']             = gID
        game['type']            = json['type']
        game['playersNo']       = 0
        game['turn']            = 1
        game['lastActivity']    = help.getTime()
        game['figurines']       = getFigurines()
        game['status']          = 'LOBBY'
        r.setGame(gID, game)
        r.init(gID)

        ret         = join(json, gID)
        return ret
    except:
        ret             = {}
        ret['error']    = 'host'
        return ret

def join(json, gID=None):                                                   #sets a player
    ret = {}
    if gID == None:
        gID                                 = json['gID']
    try:
        game                                = r.getGames()[gID]
        if game['playersNo'] == 8:
            ret['error']                    = 'full'
        else:
            game['playersNo']               += 1
            uID                             = help.genID()
            player                          = {}
            player['uID']                   = uID
            player['money']                 = 10000                         # TODO fix
            player['public']                = {}
            player['public']['name']        = json['name']
            player['public']['number']      = game['playersNo']
            player['public']['properties']  = {}
            player['public']['GOOJF']       = 0
            player['public']['position']    = 0
            r.setPlayer(gID, uID, player)
            r.setGame(gID, game)
            ret['player']                   = player
            ret['game']                     = game
            ret['players']                  = {}
            players                         = r.getPlayers(json['gID'])
            for _uID in players:
                ret['players'][players[_uID]['public']['name']] = players[_uID]['public']
    except:
        ret['error'] = 'join'
    return ret

def selectFigurine(json):                                                   #used in lobby to select players figurine
    ret     = {}
    game    = r.getGames()[json['gID']]

    if json['figurine'] in game['figurines']:

        player                          = r.getPlayer(json['gID'], json['uID'])
        player['public']['figurine']    = json['figurine']

        game['figurines'].remove(json['figurine'])
        r.setPlayer(json['gID'], json['uID'], player)
        r.setGame(json['gID'], game)

        ret['player']       = player
        ret['game']         = game
        ret['players']      = {}

        players = r.getPlayers(json['gID'])
        for _uID in players:
            ret['players'][players[_uID]['public']['name']] = players[_uID]['public']
    else:
        ret['error']        = 'figurine'
    return ret

def getGameStatus(gID):
    return r.getGame(gID)['status']

def ping(json):
    ret             = {}
    ret['game']     = r.getGame(json['gID'])
    players         = r.getPlayers(json['gID'])
    ret['player']   = players[json['uID']]
    ret['players'] = {}
    for _uID in players:
        ret['players'][players[_uID]['public']['name']] = players[_uID]['public']
    return ret

def lobby(json):
    if 'gID' in json and 'uID' in json:                                 # if user has valid uID and gID
        if r.validateUID(json['gID'], json['uID']):

            if json['request'] == 'FIGURINE':                           # user selecting figurine
                ret = selectFigurine(json)
            elif json['request'] == 'PING':                             # user polling for details
                ret = ping(json)

    elif 'gID' in json and 'uID' not in json and json['request'] == 'JOIN':
        if r.validateGID(json['gID']):                                  # set join user details
            ret = join(json)

    else:
        if json['request'] == 'HOST':                                   # set host user details
            ret = host(json)

    return ret