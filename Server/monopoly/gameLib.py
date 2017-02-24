def move(gID, uID, diceRoll):
    #move a player and decide what happens at the destination square
    pass

def updateLocation(gID, uID, destination):
    #updates player's location on the board by calling Redis fn
    pass

def drawCard(gID, uID, cardType):
    #draws a card from the stack returns it
    pass

def parseCard(gID, uID, card):
    #decides what needs to be done with the card; returns GOOJF or None(?)
    pass

def checkPassGo(gID, uID, start, finish):
    #checks if the player has passed go in this turn
    #(if start >= 28 and finish >= 0)
    pass

def payTax(gID,uID, amount):
    #transfers money from player to bank for tax purposes
    pass

def parseProperty(gID, uID, propertyID):
    #checks if property is owned. If owned by player or owned by another but
    #currently mortgaged, do nothing & end turn. If owned by other player
    #(but not mortgaged), trigger payRent(). If available, trigger buy(),
    # which gives player option to buy or trigger auction.
    pass

def buy(gID, uID, propertyID):
    #trigger UI to give player option to buy or not.
    pass

def payRent(gID, uID, propertyID):
    #automatically deduct rent from player and pass to owner of property
    pass
