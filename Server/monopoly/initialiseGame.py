import json

def loadJSON(filename):
    with open(filename + ".json") as json_file:
        json_data = json.load(json_file)
        return json_data[filename]

def getInitialBoard():
    return loadJSON("board")
def getFigurines():
    return ["HAT", "CAR", "THIMBLE", "IRON", "BOOT", "SHIP", "DOG", "WHEELBARROW"]
def getProperties():
    return loadJSON("properties")
def getCards():
    return loadJSON("cards")
