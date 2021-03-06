import monopoly.redisLib as r
from monopoly.dice import double_roll, drawFromDeck
from monopoly import helpers
from monopoly.getData import getChanceJson, getCommChestJson
from monopoly.chat import addChat

#******************************************************************************
    #Monopoly/Helper Methods

# !If a method returns an alert, all methods that call that, must propagate the alert so it makes it's way to the first method!

# TODO: Debug with unit test

# Methods to write:
#   forceTurn (can also be used for debugging)

#******************************************************************************

def gameOver(gID):
    return len(r.getGame(gID)["spect"]) == r.getGame(gID)["playersNo"] - 1

def killPlayer(gID, uID):
    game = r.getGame(gID)
    players = r.getPlayers(gID)
    players[uID]["options"] = []
    players[uID]["state"] = "spect"
    game["spect"].append(players[uID]["public"]["number"])
    r.setGame(gID, game)
    r.setPlayers(gID, players)

def measureAssets(gID, uID, amountNeeded):
    alert               = {}
    alert["boolean"]    = False
    players             = r.getPlayers(gID)
    deeds               = r.getDeeds(gID)
    assetsTotal         = 0
    if players[uID]['money'] < amountNeeded:
        for group in players[uID]["public"]["properties"]:
            for pID in players[uID]["public"]["properties"][group]["owned"]:
                if deeds[pID]['status'] != "mortgaged":
                    assetsTotal += (deeds[pID]["house1"] * deeds[pID]['buildings']) / 2
                    assetsTotal += deeds[pID]["mortgage"]
        assetsTotal += players[uID]['money']
        if assetsTotal < amountNeeded:
            alert["boolean"] = True
            alert["alert"]   = "BANKRUPT"
            killPlayer(gID, uID)
            return alert
    return alert

def payToGOOJ(gID, uID, player):
    alert = {}
    alert['boolean'] = False
    if player['money'] > 50:
        player['money'] - 50
        r.setPlayer(gID, uID, player)
    else:
        tempAlert           = measureAssets(gID, uID, 50)
        if not tempAlert["boolean"]:
            alert['boolean']    = True
            alert["alert"]      = "INSUFFICIENT FUNDS"
        else:
            alert               = tempAlert
    return alert

def hasGOOJF(player, deckType):
    return player["public"]["GOOJF"][deckType]

def inJail(gID, uID):
    # returns True if player is in jail
    return r.getPlayers(gID)[uID]['public']['jail']['boolean']

def giveGOOJF(gID, uID, deckType):
    player  = r.getPlayers(gID)[uID]
    game    = r.getGame(gID)
    game['takenGOOJF'][deckType] = True
    player['public']['GOOJF'][deckType] = True
    r.setPlayer(gID, uID, player)
    r.setGame(gID, game)

def setDeed(gID, uID, deed):
    # sets deed to deeds
    deeds               = r.getDeeds(gID)
    deeds[deed['pID']]  = deed
    r.setDeeds(gID, deeds)

def incrementMoney(gID, uID, amount):
    # increments money for a player
    player          = r.getPlayers(gID)[uID]
    player['money'] = int(player['money']) + int(amount)
    r.setPlayer(gID, uID, player)

def decrementMoney(gID, uID, amount):
    # decrements money from player
    player          = r.getPlayers(gID)[uID]
    player['money'] = int(player['money']) - int(amount)
    r.setPlayer(gID, uID, player)

def rentCalculator(gID, property):
    # calculates rent for a specific property <deed>
    playerProp  = None
    players     = r.getPlayers(gID)
    for _uID in players:
        if players[_uID]['public']['number'] == property['owner']:
            playerProp = players[_uID]['public']['properties']
            break
    if property["group"] == "transport":
        rentFactor  = 2 ** (len(playerProp[property["group"]]["owned"]) - 1)
        rent        = property["rent"] * rentFactor
    elif property["group"] == "services":
        game        = r.getGame(gID)
        rollValue   = game["lastRoll"]["value"]
        if len(playerProp[property["group"]]["owned"]) == 1:
            rent = rollValue*4
        else:
            rent = rollValue*10
    elif property['buildings'] > 0:
        if property["buildings"] == 5:
            rent = property["hotel"]
        else:
            rent = property["house" + str(property['buildings'])]
    else:  
        rent = property['rent']
        if len(playerProp[property['group']]['owned']) == playerProp[property['group']]['size']:
            rent = rent * 2
    return rent

def pay(gID, uID, rec, amount):
    #pay to a player/bank (rec == 0 for bank), !can return an alert!
    alert     = {}
    alert['boolean']    = False
    players   = r.getPlayers(gID)
    if players[uID]['money'] >= amount:
        players[uID]['money'] = players[uID]['money'] - amount
        if rec != 0:
            for _uID in players:
                if players[_uID]['public']['number'] == rec:
                    players[_uID]['money'] += amount
                    r.setPlayer(gID, _uID, players[_uID])
        r.setPlayer(gID, uID, players[uID])
    else:
        tempAlert = measureAssets(gID, uID, amount)
        if not tempAlert["boolean"]:
            alert['boolean']    = True
            alert['alert']      = "INSUFFICIENT FUNDS"    # alert; must be dealt with or player loses
        else:
            alert = tempAlert
    return alert

def isMortgageable(gID, pID, playerNo):
    # returns boolean if property is mortgageable
    alert = {}
    deeds = r.getDeeds(gID)
    alert['value'] = False
    if deeds[pID]['owner'] == playerNo:
        for _pID in deeds:
            if deeds[_pID]['group'] == deeds[pID]['group']:
                if deeds[_pID]['buildings'] == None:
                    alert['value'] = "CANNOT MORTGAGE. SELL PROPERTY."
                    break
    return alert

def housingShortage(gID):
    # returns true if there are no houses to be bought
    return r.getGame(gID)['buildings'] != 0

def hasMonopoly(gID, uID, group):
    # returns True if player has a monopoly on group
    player = r.getPlayers(gID)[uID]
    return len(player['public']['properties'][group]['owned']) == player['public']['properties'][group]['groupSize']

def canBuild(gID, uID, pID, dem=False):
    # returns True if a player can build/demolish
    deeds               = r.getDeeds(gID)
    deed                = deeds['pID']
    canBuild = False
    if not housingShortage(gID) and hasMonopoly(gID, uID, deed['group']):
        canBuild = True
        if deed['group'] != "service" or deed['group'] != "transport":
            propertyBuildings   = []
            for _pID in deeds:
                if deeds[_pID]['group'] == deed['group']:
                    propertyBuildings.append(deeds[_pID]['buildings'])
            canBuild = canBuild and (max(propertyBuildings) - min(propertyBuildings) <= 1)
            if dem:
                canBuild = canBuild and (deed['buildings'] == max(propertyBuildings)) and (deed['buildings'] != 0)
            else:
                canBuild = canBuild and (deed['buildings'] == min(propertyBuildings)) and (deed['buildings'] != 5)
    return canBuild

def processCard(gID, uID, card, deckType):
    alert = {}
    alert['boolean'] = False
    if card['type'] == "GOOJF":
        giveGOOJF(gID, uID, deckType)
        return alert
    if card['type'] == "move":
        if int(card['destination']) == 10:
            alert = updateLocation(gID, uID, "GTJ", card=True) 
        else:
            alert = updateLocation(gID, uID, int(card['destination']), card=True)
    elif card['type'] == "pay":
        alert = pay(gID, uID, 0, card['amount'])
    elif card['type'] == "receive":
        incrementMoney(gID, uID, card['amount'])

    return alert

def drawCard(gID, uID):
    alert = {}
    alert['boolean'] = False
    game        = r.getGame(gID)
    board       = r.getBoard(gID)
    player      = r.getPlayers(gID)[uID]
    pos         = player['public']['position']
    cardType    = board[pos]['name']
    cardNumber  = drawFromDeck()
    takenGOOJF  = game['takenGOOJF'][cardType]
    if takenGOOJF and cardNumber == 0:
        cardNumber += 1
    if cardType == "CommunityChest":
        deck = getCommChestJson()
    else:
        deck = getChanceJson()

    deck            = helpers.keyStringtoInt(deck)
    card            = deck[cardNumber - 1]
    alert           = processCard(gID, uID, card, cardType)
    alert['card']   = card

    return alert

def analysePosition(gID, uID, board, pos):
    # analyses the player's position to see what operations need to be made on a square
    alert               = {}
    alert['boolean']    = False
    square              = board[pos]
    if square['category'] == 'tax':
        alert = pay(gID, uID, 0, square['amount'])             #pay the bank the tax amount required on this square
        return alert

    if square["category"] == "special":
        if square['name'] == 'goToJail':
            alert = updateLocation(gID, uID, "GTJ")

    elif square['category'] == 'card':
        alert = drawCard(gID, uID)
        
    elif square['category'] == 'property':
        deed = r.getDeeds(gID)[square['pID']]
        if deed['status'] == "owned":
            rent    = rentCalculator(gID, deed)
            alert   = pay(gID, uID, deed['owner'], rent)
            alert["activity"] = "rent"
            return alert
        elif deed['status'] == "mortgaged":
            pass
        elif deed['status'] == "notOwned":
            player = r.getPlayers(gID)[uID]
            player['options'] += ["BUY"]
            player['options'] += ["AUCTION"]
            player["canBuy"]   = square["pID"]
            r.setPlayer(gID, uID, player)
    return alert

def updateLocation(gID, uID, value, card=False):         #moves a player to new position
    #value can be value of a roll, or a special card e.g. jail, go, free parking
    player  = r.getPlayers(gID)[uID]
    board   = r.getBoard(gID)
    prevPos = player['public']['position']
    GO      = False
    if value == "GTJ":
        newPos = 10
        player['public']['jail']['boolean'] = True
        alert = {}

        alert['boolean']    = True
        alert['alert']      = "IN JAIL"

        board[prevPos]['playersOn'].remove(player["public"]['number'])
        board[newPos]['playersOn'].append(player["public"]['number'])

        r.setBoard(gID, board)
        player['public']['position'] = newPos
        r.setPlayer(gID, uID, player)
        return alert

    if card:
        newPos = int(value)
        if newPos > 39:
            game = r.getGame(gID)
            amount = game['GO']
            incrementMoney(gID, uID, amount)
            newPos = newPos - 40
            GO      = True
    else:
        newPos  = prevPos + value
        if newPos > 39:
            game = r.getGame(gID)
            amount = game['GO']
            incrementMoney(gID, uID, amount)
            newPos = newPos - 40
            GO      = True

    board[prevPos]['playersOn'].remove(player['public']['number'])
    board[newPos]['playersOn'].append(player['public']['number'])

    r.setBoard(gID, board)
    player['public']['position'] = newPos
    r.setPlayer(gID, uID, player)

    alert = analysePosition(gID, uID, board, newPos)     #checking position
    if GO:
        alert["GO"] = GO
    return alert

def checkTurn(gID, uID):
    #checks to see if it's the player's turn
    game    = r.getGame(gID)
    player  = r.getPlayers(gID)[uID]
    if (player['public']['number'] == game['turn']):
        if player['state'] == 'spect':
            incrementTurn(gID)
            checkTurn(gID, uID)
        return True
    else:
        return False

def incrementTurn(gID):
    # goes to next turn (also accounts for double rolls)
    game = r.getGame(gID)
    if not game['lastRoll']['double']:
        turn = game['turn'] + 1
        if turn > game['playersNo']:
            turn = turn - game['playersNo']
        game['turn'] = turn
        r.setGame(gID, game)
        return True
    else:
        return False

def mCannotTrade(gID, sender, receiver, jOffer, jFor):
    alert = {}
    alert["boolean"] = False
    sTotal = 0
    rTotal = 0
    if "property" in jOffer or "property" in jFor:
        deeds  = r.getDeeds(gID)
        if "property" in jOffer:
            for pID in jOffer["property"]:
                if deeds[pID]["status"] == "mortgaged":
                    sTotal += deeds[pID]["mortgage"]/10
        if "property" in jFor:
            for pID in jFor["property"]:
                if deeds[pID]["status"] == "mortgaged":
                    rTotal += deeds[pID]["mortgage"]/10
    sMortgage = sTotal
    rMortgage = rTotal
    sTotal    = 0
    rTotal    = 0
    if "money" in jOffer:
        sTotal += jOffer["money"] - sMortgage
    if "money" in jFor:
        rTotal += jFor["money"] - rMortgage
    if rTotal != 0 or sTotal != 0:
        if sTotal > rTotal :
            if sTotal < sTotal - rTotal:
                alert["alert"]      = "INSUFFICENT FUNDS"
                alert["boolean"]    = True
            else:
                pass
        elif sTotal < rTotal:
            if rTotal < rTotal - sTotal:
                alert["alert"]      = receiver['public']['name'] + "CANNOT MAKE THIS DEAL AT THIS TIME"
                alert["boolean"]    = True
            else:
                pass
    if not alert["boolean"]:
        alert["sTotal"]     = sTotal
        alert["rTotal"]     = rTotal
        alert["sMortgage"]  = sMortgage
        alert["rMortgage"]  = rMortgage
    return alert

def pCannotTrade(gID, jOffer, jFor):
    alert = {}
    alert["boolean"] = False
    if "property" in jOffer or "property" in jFor:
        deeds = r.getDeeds(gID)
        for pID in deeds:
            if deeds[pID] in jOffer["property"] or deeds[pID] in jFor["property"]:
                if deeds[pID]["buildings"] > 0:
                    alert["boolean"] = True
                    alert["alert"] = "CANNOT SELL DEVELOPED PROPERTY"
                    return alert
    return alert

def initTrade(gID, uID, playerNumber, jOffer, jFor):
    alert               = {}
    alert["boolean"]    = False
    game                = r.getGame(gID)
    players             = r.getPlayers(gID)
    trader              = players[uID]
    receiver            = None
    _uID                = None
    for ID in players:
        if players[ID]['public']['number'] == playerNumber:
            receiver = players[ID]
            _uID     = ID

    alert = mCannotTrade(gID, trader, receiver, jOffer, jFor)["boolean"]
    if not alert["boolean"]:
        alert = pCannotTrade(gID, jOffer, jFor)

    if not alert["boolean"]:
        tID                             = helpers.genID()
        offer                           = {}
        offer["from"]                   = {}
        offer["to"]                     = {}
        offer["from"]["number"]         = trader['public']['number']
        offer["from"]["name"]           = trader['public']['name']
        offer["to"]["number"]           = receiver['public']['number']
        offer["to"]["name"]             = receiver['public']['name']
        offer['offered']                = jOffer
        offer['for']                    = jFor
        game['trade'][tID]              = offer
        trader["trade"]["sent"][tID]    = {"pending":receiver["public"]["name"]}
        receiver["trade"]["recieved"]   += tID
        r.setPlayer(gID, _uID, receiver)
        r.setPlayer(gID, uID, trader)
        r.setGame(gID, game)
    return alert

def giveProperty(gID, uID, deed, status="owned"):
    # method for giving a player a property (deed signing)
    player              = r.getPlayers(gID)[uID]
    deed['status']      = status
    deed['owner']       = player['public']['number']
    player['public']['properties'][deed['group']]['owned'].append(deed['pID'])
    r.setDeed(gID, deed["pID"], deed)
    r.setPlayer(gID, uID, player)

def tradeProp(gID, aUID, bUID, pID, aPlayer, bPlayer):
    deed    = r.getDeeds(gID)[pID]
    bPlayer['public']["properties"][deed["group"]].remove(pID)
    r.setPlayer(gID, bUID, bPlayer)
    giveProperty(gID, aUID, aPlayer, deed, deed["status"])

def acceptTrade(gID, uID, tID):
    alert               = {}
    alert["boolean"]    = False
    game                = r.getGame(gID)
    trade               = game['trade'][tID]
    players             = r.getPlayers(gID)
    player              = players[uID]
    _uID                = None
    sendingPlayer       = trade[tID]["from"]["number"]
    for ID in players:
        if players[ID]['public']["number"] == sendingPlayer:
            sendingPlayer   = players[ID]
            _uID            = ID
            break

    alert = mCannotTrade(gID, sendingPlayer, player, trade["offered"], trade["for"])
    if not alert["boolean"]:
        sTotal = alert["sTotal"]
        rTotal = alert["rTotal"]
        decrementMoney(gID, uID, alert["rMortgage"])
        decrementMoney(gID, _uID, alert["sMortgage"])
        if sTotal > rTotal:
            alert = pay(gID, _uID, sendingPlayer["public"]["number"], sTotal - rTotal)
        elif rTotal > sTotal:
            alert = pay(gID, uID, player["public"]["number"], rTotal - sTotal)

    if "property" in trade["offered"]:
        for pID in trade["offered"]["property"]:
            tradeProp(gID, uID, _uID, pID, player, sendingPlayer)
    if "property" in trade["for"]:
        for pID in trade["for"]["property"]:
            tradeProp(gID, _uID, uID, pID, sendingPlayer, player)

    if "GOOJF" in trade["offered"]:
        sendingPlayer["public"]["GOOJF"][trade["offered"]["GOOJF"]] = False
        giveGOOJF(gID, uID, trade["offered"]["GOOJF"])
    if "GOOJF" in trade["for"]:
        player["public"]["GOOJF"][trade["for"]["GOOJF"]] = False
        giveGOOJF(gID, _uID, trade["for"]["GOOJF"])

    if not alert["boolean"]:
        sendingPlayer["trade"]["sent"][tID] = {"accepted": player["public"]["name"]}
        r.setPlayer(gID, _uID, sendingPlayer)
    return alert

def declineTrade(gID, uID, tID):
    game        = r.getGame(gID)
    players     = r.getPlayers(gID)
    player      = r.getPlayers(gID)[uID]
    sender      = game["trade"][tID]["from"]["number"]
    game["trade"].pop(tID, None)
    r.setGame(gID, game)
    _uID        = None
    for ID in players:
        if players[ID]['public']["number"] == sender:
            sender  = players[ID]
            _uID    = ID
    sender["trade"]["sent"][tID]    = {"declined": player["public"]["name"]}
    r.setPlayer(gID, _uID, sender)

#******************************************************************************
    #Controller Methods

#******************************************************************************

def mortgage(json):
    # used to mortgage a property
    gID             = json['gID']
    uID             = json['uID']
    pID             = json['pID']
    deeds           = r.getDeeds(gID)
    deed            = deeds[pID]
    player          = r.getPlayers(gID)[uID]
    mortgageable    = isMortgageable(gID, pID, player['public']['number'])
    if mortgageable['value'] == False:
        deed["status"]  = "mortgaged"
        player['money'] += deed['mortgage']
        r.setPlayer(gID, uID, player)
        r.setDeeds(gID, deeds)
        ret = helpers.getReturnData(gID, uID)
    else:
        ret = helpers.getReturnData(gID, uID, [], [], mortgageable['value'])
    return ret

def roll(json):
    # rolling a dice
    gID                 = json['gID']
    uID                 = json['uID']
    roll                = double_roll()
    game                = r.getGame(gID)
    game['lastRoll']    = roll
    r.setGame(gID, game)

    if inJail(gID, uID) and not roll['double']:
        player = r.getPlayers(gID)[uID]
        if player["public"]["jail"]["turn"] == 4:
            alert = payToGOOJ(gID, uID, player)
            if alert["boolean"]:
                #kill player
                pass
            else:
                getOutOfJail(gID, uID)
        if player["public"]["jail"]["turn"] == 3:
            alert = payToGOOJ(gID, uID, player)
            if alert["boolean"]:
                ret = helpers.getReturnData(gID, uID, ["ROLLED"], ['ROLL'], alert['alert'])
                return ret
            else:
                getOutOfJail(gID, uID)
        if inJail(gID, uID):
            player['public']['jail']['turn'] += 1
            incrementTurn(gID)
            r.setPlayer(gID, uID, player)
            ret = helpers.getReturnData(gID, uID, [], ['ROLL'])
            return ret

    elif inJail(gID, uID) and roll['double']:
        getOutOfJail(gID, uID)

    alert = updateLocation(gID, uID, roll['value'])
    if "card" in alert:
        card = alert["card"]
    else:
        card = False
    if alert['boolean']:
        ret = helpers.getReturnData(gID, uID, [], ['ROLL'], alert['alert'], card)
        if alert["alert"] == "IN JAIL":
            incrementTurn(gID)
            return ret
        else:
            return ret
    elif "activity" in alert:
        if alert['activity'] == "rent":
            ret = helpers.getReturnData(gID, uID, [], ['ROLL'], alert['activity'], card)
            incrementTurn(gID)
            return ret
    elif card == False:
        ret = helpers.getReturnData(gID, uID, ["ROLLED"], ['ROLL'])
        return ret

def buy(json):
    # if player has option to buy a certain property and chooses to buy
    gID         = json['gID']
    uID         = json['uID']
    pID         = json["pID"]
    players     = r.getPlayers(gID)
    player      = players[uID]
    if player["canBuy"] == pID:
        deed        = r.getDeeds(gID)[pID]
        alert       = pay(gID, uID, 0, deed['price'])
        if not alert['boolean']:
            giveProperty(gID, uID, deed)
            if incrementTurn(gID):
                ret = helpers.getReturnData(gID, uID, [], ["BUY", "AUCTION", "ROLLED"])
            else:
                ret = helpers.getReturnData(gID, uID, ["ROLL"], ["BUY", "AUCTION", "ROLLED"])
        else:
            ret = helpers.getReturnData(gID, uID, [], [], alert['alert'])
        return ret

def auction(json):
    # moves the game state into an auction for 30 seconds
    gID     = json['gID']
    uID     = json['uID']
    players = r.getPlayers(gID)
    player  = players[uID]
    pID     = json["pID"]
    if player["canBuy"] == pID:
        deed    = r.getDeeds(gID)[pID]
        for _uID in players:
            players[_uID]['options'] += ["BID"]
            r.setPlayer(gID, _uID, players[_uID])
        game = r.getGame(gID)
        game['auction'] = {}
        game['auction']['pID'] = pID
        game['auction']['highest']  = {0:deed['price']/2}
        game['auction']['out']      = []
        game['lastActivity']        = helpers.getTime()
        game['state']               = "AUCTION"
        r.setGame(gID, game)
        ret = helpers.getReturnData(gID, uID, [], ["AUCTION", "BUY"])
        return ret

def build(json, dem=False):
    # build/demolish
    gID = json['gID']
    uID = json['uID']
    pID = json['pID']
    if canBuild(gID, uID, pID):
        deed    = r.getDeeds(gID)[pID]
        cost    = deed['housePrice']
        if dem:
            incrementMoney(gID, uID, cost/2)
            deed['buildings'] += 1
        else:
            alert   = pay(gID, uID, 0, cost)
            if alert:
                ret = helpers.getReturnData(gID, uID, [], [], alert)
                return ret
            deed['buildings'] += 1
        setDeed(gID, uID, pID)
        ret = helpers.getReturnData(gID, uID)
    else:
        alert = "CANNOT BUILD"
        ret = helpers.getReturnData(gID, uID, [], [], alert)
    return ret

def getOutOfJail(gID, uID, card=False):
    ret = None
    if card:
        player = r.getPlayers(gID)[uID]
        if inJail(gID, uID) and (player['public']['GOOJF']['CommunityChest'] or player['public']['GOOJF']['Chance']):
            deck = None
            if player['public']['GOOJF']['CommunityChest']:
                deck = "CommunityChest"
            elif player['public']['GOOJF']['Chance']:
                deck = "Chance"
            player['public']['GOOJF'][deck] = False
            game                            = r.getGame(gID)
            game['takenGOOJF'][deck]        = False
            r.setGame(gID, game)
            ret = helpers.getReturnData(gID, uID)
        else:
            ret = helpers.getReturnData(gID, uID, [], [], "INVALID USE")
    player                              = r.getPlayers(gID)[uID]
    player['public']['jail']['boolean'] = False
    player['public']['jail']['turn']    = 0
    r.setPlayer(gID, uID, player)
    if card:
        return ret

def trade(json):
    alert               = {}
    alert["boolean"]    = False
    gID                 = json['gID']
    uID                 = json['uID']
    if json["tradeStatus"] == "init":
        alert = initTrade(gID, uID, json['playerNumber'], json["offer"], json["for"])
    elif json["tradeStatus"] == "accept":
        alert = acceptTrade(gID, uID, json["tID"])
    elif json["tradeStatus"] == "decline":
        declineTrade(gID, uID, json["tID"])

    if alert["boolean"]:
        ret = helpers.getReturnData(gID, uID, [], [], alert["alert"])
    else:
        ret = helpers.getReturnData(gID, uID)
    return ret

def ping(json, isTurn):
    if isTurn:
        player = r.getPlayers(json['gID'])[json['uID']]
        if 'ROLLED' in player['options']:
            ret  = helpers.getReturnData(json['gID'], json['uID'])
        else:
            ret  = helpers.getReturnData(json['gID'], json['uID'], ["ROLL"])
    else:
        ret  = helpers.getReturnData(json['gID'], json['uID'])
    return ret

def chat(json):
    gID             = json["gID"]
    uID             = json["uID"]
    player          = r.getPlayers(gID)[uID]
    playerName      = player["public"]["name"]
    number          = player["public"]["number"]
    addChat(gID, playerName, number, json["text"])
    ret = helpers.getReturnData(json['gID'], json['uID'])
    return ret

def payGetOutOfJail(gID, uID):
    players = r.getPlayers(gID)
    player  = players[uID]
    alert   = payToGOOJ(gID, uID, player)
    if alert["boolean"] == False:
        getOutOfJail(gID, uID)
        ret = helpers.getReturnData(gID, uID)
    else:
        ret = helpers.getReturnData(gID, uID, [], [], alert["alert"])
    return ret

def payMort(json):
    gID             = json["gID"]
    uID             = json["uID"]
    pID             = json['pID']
    deeds           = r.getDeeds(gID)
    deed            = deeds[pID]
    mortgageAmount  = int(deed["mortgage"] * 1.1)
    alert           = pay(gID, uID, 0, mortgageAmount)
    if alert["boolean"]:
        ret = helpers.getReturnData(gID, uID, [], [], alert['alert'])
    else:
        deeds[pID]["status"] = "owned"
        r.setDeeds(gID, deeds)
        ret = helpers.getReturnData(gID, uID)
    return ret

#******************************************************************************
    # Flask Game + Bid Controller Abstraction
#******************************************************************************

def game(json):
    ret = {'error':'game'}
    isTurn = checkTurn(json['gID'], json['uID'])
    if r.validateUID(json['gID'], json['uID']):
        if json['request'] == "PING":
            ret = ping(json, isTurn)
        if json['request'] == "CHAT":
            ret = chat(json)

        elif isTurn and json['request'] in r.getPlayers(json['gID'])[json['uID']]['options']:
            if "ROLLED" not in r.getPlayers(json['gID'])[json['uID']]['options'] and json['request'] == "ROLL":
                ret = roll(json)
            elif json['request'] == 'BUY':
                ret = buy(json)
            elif json['request'] == 'AUCTION':
                ret = auction(json)


        elif json['request'] == 'MORTGAGE':
            ret = mortgage(json)
        elif json['request'] == "BUILD":
            ret = build(json)
        elif json['request'] == 'SELL':
            ret = build(json, True)
        elif json['request'] == 'TRADE':
            ret = trade(json)
        elif json['request'] == 'GOOJF':
            ret = getOutOfJail(json['gID'], json['uID'], True)
        elif json['request'] == 'PAYMORT':
            ret = payMort(json)
        elif json["request"] == "PGOOJ":
            ret = payGetOutOfJail(json['gID'], json['uID'])

        if gameOver(json['gID']):
            game            = r.getGame(json['gID'])
            game['state']   = "FINISHED"
            r.setGame(json["gID"], game)

        return ret

def bid(json):
    gID = json['gID']
    uID = json['uID']
    if r.validateUID(json['gID'], json['uID']):
        game        = r.getGame(gID)
        players     = r.getPlayers(gID)
        player      = players[uID]
        hBidder     = None
        for key in game['auction']['highest']:
            hBidder = key
        hBidAmount  = game['auction']['highest'][hBidder]

        def close():
            if hBidder == None or int(hBidder) == 0:
                for _uID in players:
                    players[_uID]['options'].remove("BID")
                    if "AUCTION" in players[_uID]["options"]:
                        players[_uID]['options'].remove("AUCTION")
                    if "BUY" in players[_uID]["options"]:
                        players[_uID]['options'].remove("BUY")
                        players[_uID]["canBuy"] = None
                r.setPlayers(gID, players)
                game['state'] = "PLAYING"
                r.setGame(gID, game)
                incrementTurn(gID)
                return helpers.getReturnData(gID, uID)
            if int(hBidder) != 0:
                payUID = None
                for _uID in players:
                    if players[_uID]["public"]["number"] == int(hBidder):
                        payUID = _uID
                        break
                alert = pay(gID, payUID, 0, hBidAmount)
                if not alert['boolean']:
                    deed = r.getDeeds(gID)[game['auction']['pID']]
                    giveProperty(gID, payUID, deed)
                    for _uID in players:
                        players[_uID]['options'].remove("BID")
                        if "AUCTION" in players[_uID]["options"]:
                            players[_uID]['options'].remove("AUCTION")
                        if "BUY" in players[_uID]["options"]:
                            players[_uID]['options'].remove("BUY")
                            players[_uID]["canBuy"] = None
                    r.setPlayers(gID, players)
                    game['state'] = "PLAYING"
                    r.setGame(gID, game)
                    incrementTurn(gID)
                    return helpers.getReturnData(gID, uID)
                else:
                    return helpers.getReturnData(gID, uID, [], [], alert['alert'])

        if not helpers.checkTime(game['lastActivity'], 30, True):
            return close()

        elif json['request'] == "PING":
            pass

        elif json['request'] == "BID" and player['public']['number'] not in game['auction']['out']:
            if (json['amount'] > hBidAmount) and (json['amount'] <= player['money']):
                newBid                      = {player['public']['number'] : json['amount']}
                game['auction']['highest']  = newBid
                r.setGame(json['gID'], game)
            else:
                return helpers.getReturnData(gID, uID, [], [], "INSUFFICIENT FUNDS")

        elif json['request'] == "OUT":
            if hBidder != player['public']['number']:
                game['auction']['out'].append(player['public']['number'])
                r.setGame(json['gID'], game)
                if len(game['auction']['out']) >= game['playersNo'] - 1 - len(game['spect']):
                    return close()

        return helpers.getReturnData(gID, uID)