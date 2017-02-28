import json

def loadJSON(filename):
    with open(filename + ".json") as json_file:
        json_data = json.load(json_file)
        return json_data[filename]

def keyStringtoInt(dictionary):
    # convert all top level dict string keys to ints
    # eg {"0":"abc} -> {0:"abc"}
    return {int(k):v for k,v in dictionary.items()}

def getInitialBoard():
    # return the contents of board.json as a python dict,
    # with (JSON required) string keys converted to int
    return keyStringtoInt(loadJSON("board"))

def getCards():
    # return contents of cards.json as python dict
    cards = loadJSON("cards")
    chance = keyStringtoInt(cards['Chance'])
    communityChest = keyStringtoInt(cards['CommunityChest'])
    return {"Chance": chance, "CommunityChest" : communityChest}

def getFigurines():
    return ["HAT", "CAR", "THIMBLE", "IRON", "BOOT", "SHIP", "DOG", "WHEELBARROW"]
def getProperties():
    return loadJSON("properties")

