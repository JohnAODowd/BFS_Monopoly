import monopoly.redisLib as r
from monopoly.dice import double_roll
import monopoly.helpers as help

#******************************************************************************
    #Monopoly/Helper Methods
#******************************************************************************

def pay(gID, sender, receiver, amount):             
    #pay to a player/bank (receiver == 0 for bank), can return an alert
    ret         = {}
    player     = r.getPlayer(gID,sender)
    if player['money'] >= amount:
        r.decrementMoney(gID,sender,amount)
        r.incrementMoney(gID,receiver,amount)
        #ret...notice of amount transferred 
    else:
        ret['alert'] = "INSUFFICIENT FUNDS"    # alert; must be dealt with or player loses
    return ret
    
    

def analysePosition(gID, uID, board, position):
    # analyses the player's position to see what operations need to be made on a square
    
    if board[pos]['category'] == 'tax':
        pay(gID,uID,0,square['amount']) #pay the bank the tax amount required on this square
        pass
    
    elif board[pos]['category'] == 'special':
        if square['name'] == 'Free Parking' or square['name'] == 'Jail' or square['name'] == 'Go':
            # do nothing
            pass
        if square['name'] == 'Go To Jail':
            goToJail(gID,uID)
        
    elif board[pos]['category'] == 'card':
        drawCard(gID, uID, square['name'])
        
    elif board[pos]['category'] == 'property':
        if board[pos]['property']['status'] == "owned":
            ret = pay(gID, uID, board[pos]['property']['owner'], board[pos]['property']['rent'])
        elif board[pos]['property']['status'] == "mortgaged":
            pass
        else:
            ret                 = {}
            ret['options']      = ['BUY', 'AUCTION']
            player              = r.getPlayer(gID, uID)
            player['options']   += ["BUY"]      #why?
            player['options']   += ["AUCTION"]  #why?
            return ret
            
    else:
        ret             = {}
        ret['ignore']   = board[pos]['category']    #why?
    return ret

def updateLocation(gID, uID, value):         #moves a player to new position
    ret         = {}
    player      = r.getPlayer(gID, uID)
    board       = r.getBoard(gID)
    previousPosition     = player['public']['position']
    newPosition      = prevPosition + value
    if newPosition > 39:
        newPosition = newPosition - 40
    board[prevPosition]['playersOn'].remove(player['number'])
    board[newPosition]['playersOn'].append(player['number'])
    r.setBoard(gID, board)
    player['public']['position'] = newPosition
    r.setPlayer(gID, uID, player)           #checking position

    ret = analysePosition(gID, uID, board, newPosition)
    ret['board']    = board
    ret['player']   = player

    return ret

def checkTurn(gID, uID):
    game    = r.getGame(gID)
    player  = r.getPlayer(gID, uID)
    if player['number'] == game['turn']:
        return True
    else:
        return False

#******************************************************************************
    #Controller Methods

def getReturnData(gID, uID, options):
    ret                 = {}
    game                = r.getGame(gID)
    board               = r.getBoard(gID)
    players             = r.getPlayers(gID)
    player              = players[uID]
    if len(options):
        for option in options:
            player['options'].append(option)
        r.setPlayer(gID, uID)
    ret['options']      = player['options']
    ret['game']         = game
    ret['player']       = player
    ret['board']        = board
    ret['players']      = {}
    for _uID in players:
        ret['players'][players[_uID]['public']['name']] = players[_uID]['public']
    return ret
#******************************************************************************

def mortgage(json):
    gID     = json['gID']
    uID     = json['uID']
    player  = r.getPlayer(gID, uID)
    board   = r.getBoard(gID)
    if json['property']['id'] in player['public']['property']:
        if player['public']['property'][json['property']['id']]['status'] != "mortgaged":
            player['money'] += player['public']['property'][json['property']['id']]['mortgage']
            player['public']['property'][json['property']['id']]['status'] = "mortgaged"
            r.setPlayer(gID, uID)


def roll(json):
    gID                 = json['gID']
    uID                 = json['uID']
    roll                = double_roll()
    ret                 = updateLocation(gID, uID, roll['value'])

    game                = r.getGame(gID)
    if roll['double']  == True:
        game['double']  = True
        r.setGame(gID, game)
    players             = r.getPlayer(gID, uID)
    player              = players[uID]
    player['options'].remove("ROLL")
    r.setPlayer(gID, uID, player)
    ret['player']       = player
    ret['players']      = {}
    for _uID in players:
        ret['players'][players[_uID]['public']['name']] = players[_uID]['public']
    return ret

def buy(json):                          # if player has option to buy a certain property and chooses to buy
    gID         = json['gID']
    uID         = json['uID']
    board       = r.getBoard(gID)
    players     = r.getPlayers(gID)
    player      = players[uID]
    price       = board[player['public']['position']]['property']['price']
    ret         = pay(gID, uID, 0, price)
    if len(ret) == 0:
        player['public']['properties'] = board[player['public']['position']]['property']['id']
        board[player['public']['position']]['property']['status'] = 'owned'
        player['options'].remove('BUY')
        r.setBoard(gID, board)
        r.setPlayer(gID, uID, player)
        game = r.getGame(gID)
        if not game['double']:
            turn = game['turn'] + 1
            if turn > 8:
                turn = turn - 8
            game['turn'] = turn
        ret['game']      = game

    ret['player']   = player
    ret['board']    = board
    ret['options']  = player['options']
    ret['players']  = {}
    for _uID in players:
        ret['players'][players[_uID]['public']['name']] = players[_uID]['public']
    return ret

def auction(json):
    gID     = json['gID']
    uID     = json['uID']
    board   = r.getBoard(gID)
    players = r.getPlayers(gID)
    player  = players[uID]
    for _player in players:
        _uID = _player['uID']
        _player['options'] += ["BID"]
        r.setPlayer(gID, _uID, _player)
    game = r.getGame(gID)
    game['auction'] = {}
    game['auction']['property'] = board[player['public']['position']]['property']
    game['auction']['highest']  = board[player['public']['position']]['property']['price']/2
    game['auction']['out']      = []
    game['lastActivity']        =  help.getTime()
    game['status']              = "AUCTION"
    r.setGame(gID, game)

def ping(json, isTurn):
    if isTurn:
        ret  = getReturnData(json['gID'], json['uID'], ["ROLL"])
    else:
        ret  = getReturnData(json['gID'], json['uID'], [])
    return ret

#******************************************************************************
    # Flask Game + Bid Controller Abstraction
#******************************************************************************


def game(json):
    isTurn = checkTurn(json['gID', json['uID']])
    if r.validateUID(json['gID'], json['uID']):
        if json['request'] == "PING":
            ret = ping(json, isTurn)
        elif isTurn and json['request'] in r.getPlayer(json['gID'], json['uID'])['options']:
            if json['request'] == "ROLL":
                ret = roll(json)
            elif json['request'] == 'BUY':
                ret = buy(json)
            elif json['request'] == 'AUCTION':
                ret = auction(json)
            elif json['request'] == 'MORTGAGE':
                ret = mortgage(json)
            # elif json['request'] == 'TRADE':

        return ret

def bid(json):
    if r.validateUID(json['gID'], json['uID']):
        ret = {}
        game = r.getGame(json['gID'])
        player = r.getPlayer(json['gID'], json['uID'])


        def close():
            pass
            #move property to highest bidder/cleanup

        if not help.checkTime(game['lastActivity'], 30, True):
            close()

        elif json['request'] == "BID":
            if json['amount'] > game['auction']['highest']:
                game['auction']['highest'] = json['amount']
                game['bidder'] = player['public']['number']
                r.setGame(json['gID'], game)

        elif json['request'] == "OUT":
            if game['bidder'] != player['public']['number']:
                game['auction']['out'].append(player['public']['number'])
                r.setGame(json['gID'], game)
                if len(game['auction']['out']) > 7:
                    close()

        elif json['request'] == "PING":
            pass

        ret['game'] = game
        return ret
