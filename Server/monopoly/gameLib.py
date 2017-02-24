import monopoly.redisLib as r
from monopoly import lobby

def checkTurn(gID, uID):
    game    = r.getGame(gID)
    player  = r.getPlayer(gID, uID)
    if player['number'] == game['turn']:
        return True
    else:
        return False

def ping(json, isTurn):
    ret             = {}
    ret['game']     = r.getGame(json['gID'])
    ret['board']    = r.getBoard(json['gID'])
    players         = r.getPlayers(json['gID'])
    ret['options']  = ["MORTGAGE", "TRADE"]
    if isTurn:
        ret['options'] += ["ROLL"]
        players[json['uID']]['options'] = ret['options']
        r.setPlayer(json['gID'], json['uID'], players[json['uID']])
    ret['player']   = players[json['uID']]
    ret['players']  = {}
    for _uID in players:
        ret['players'][players[_uID]['public']['name']] = players[_uID]['public']

    return ret


def game(json):
    isTurn = checkTurn(json['gID', json['uID']])
    if r.validateUID(json['gID'], json['uID']):
        if json['request'] == "PING":
            ret = ping(json, isTurn)
        elif isTurn and json['request'] in r.getPlayer(json['gID'], json['uID'])['options']:
            if json['request'] == "ROLL":
                ret = roll(json)
            elif json['request'] == 'BUY':

            elif json['request'] == 'AUCTION':

            elif json['request'] == 'MORTGAGE':

            elif json['request'] == 'TRADE':






