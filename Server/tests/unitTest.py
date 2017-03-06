import json
import requests
from monopoly.emojiToken import generateEmoji

def post(d):
	js = d
	payload = json.dumps(js)
	headers = {'Content-Type' : 'application/json'}
	r = requests.post("http://leela.netsoc.co:8080/game", data=payload, headers=headers)
	return r.text

class user:

    _gID        = None
    _uID        = None
    _name       = None
    _figurine   = None
    _figurines  = []
    _options    = []
    _history    = None
    _data       = None
    _dic        = None
    _state      = None
    _pID        = None

    def __init__(self, name, type="HOST", gID=None):
        self._name      = name
        self._history   = "Request history: ***************************\n\n"
        if type != "HOST":
            self._gID = gID

    def __str__(self):
        string = "Name: " + str(self._name) + "\n"
        string += "gID: " + str(self._gID) + "\n"
        string += "uID: " + str(self._uID) + "\n"
        string += "figurine: " + str(self._figurine) + "\n"
        string += "\n" + self._history
        string += "\n*****************************"
        return string

    def clearHistory(self):
        self._history   = "Request history: ***************************\n\n"

    def parseResponse(self, dic):
        try:
            game            = dic["game"]
            player          = dic["player"]
            self._options   = dic["options"]
            self._state     = game["state"]
            self._pID       = player["canBuy"]
            # toPrint = "name: " + player["public"]["name"] + "\n"
            # toPrint += "position: " + str(player["public"]["position"]) + "\n"
            # toPrint += "money: " + str(player["money"]) + "\n\n"
            # if self._pID != None:
            #     print(self._name + " can buy " + self._pID)
            # print(toPrint)
        except:
            # print(dic)
            self.ping()

    def host(self):
        js                  = {}
        js["request"]       = "HOST"
        js["name"]          = self._name
        js["type"]          = "private"
        self._history       += "SENDING (HOST)*****\n" + str(js) + "\n\n"
        response            = post(js)
        self._history       += "RECIEVED***********\n" + response + "\n\n"
        response            = json.loads(response)
        print(response)
        self._gID           = response["game"]["gID"]
        self._options       = response["options"]
        self._figurines     = response["game"]["figurines"]
        self._uID           = response["player"]["uID"]

    def join(self):
        if self._gID != None:
            js                  = {}
            js["request"]       = "JOIN"
            js["name"]          = self._name
            js["gID"]           = self._gID
            self._history       += "SENDING (JOIN)*****\n" + str(js) + "\n\n"
            response            = post(js)
            self._history       += "RECIEVED***********\n" + response + "\n\n"
            response            = json.loads(response)
            self._options       = response["options"]
            self._figurines     = response["game"]["figurines"]
            self._uID           = response["player"]["uID"]

    def getGID(self):
        return self._gID

    def getUID(self):
        return self._uID

    def selectFigurine(self):
        figurines = self._figurines
        if figurines != None and len(figurines) > 0:
            figurine            = figurines[0]
            js                  = {}
            js["request"]       = "FIGURINE"
            js["figurine"]      = figurine
            js["uID"]           = self._uID
            js["gID"]           = self._gID
            self._history       += "SENDING (FIGURINE)*\n" + str(js) + "\n\n"
            response            = post(js)
            self._history       += "RECIEVED***********\n" + response + "\n\n"
            response            = json.loads(response)
            self._figurine      = response["player"]["public"]["figurine"]
            self.parseResponse(response)

    def ping(self):
        js                  = {}
        js["request"] = "PING"
        js["uID"] = self._uID
        js["gID"] = self._gID
        self._history       += "SENDING (PING)*****\n" + str(js) + "\n\n"
        response            = post(js)
        self._history       += "RECIEVED***********\n" + response + "\n\n"
        self.parseResponse(json.loads(response))

    def start(self):
        if "START" in self._options:
            js = {}
            js["request"] = "START"
            js["uID"] = self._uID
            js["gID"] = self._gID
            self._history += "SENDING (START)*\n" + str(js) + "\n\n"
            response = post(js)
            self._history += "RECIEVED***********\n" + response + "\n\n"
            self.parseResponse(json.loads(response))

    def chat(self):
        if self._state == "PLAYING":
            js = {}
            js["request"] = "CHAT"
            js["uID"] = self._uID
            js["gID"] = self._gID
            js["text"] = generateEmoji()
            self._history += "SENDING (CHAT)*\n" + str(js) + "\n\n"
            response = post(js)
            self._history += "RECIEVED***********\n" + response + "\n\n"
            self.parseResponse(json.loads(response))

    def canRoll(self):
        return "ROLL" in self._options

    def canBuy(self):
        return "BUY" in self._options

    def roll(self):
        if self.canRoll():
            js = {}
            js["request"] = "ROLL"
            js["uID"] = self._uID
            js["gID"] = self._gID
            self._history += "SENDING (ROLL)*\n" + str(js) + "\n\n"
            response = post(js)
            self._history += "RECIEVED***********\n" + response + "\n\n"
            self.parseResponse(json.loads(response))
            # toPrint = self._name + "has Rolled\n\n"
            # print(toPrint)

    def buy(self):
        if self.canBuy():
            pID = self._pID
            js = {}
            js["request"] = "BUY"
            js["uID"] = self._uID
            js["gID"] = self._gID
            js['pID'] = pID
            self._history += "SENDING (BUY)*****\n" + str(js) + "\n\n"
            response = post(js)
            self._history += "RECIEVED***********\n" + response + "\n\n"
            self.parseResponse(json.loads(response))
            # toPrint = self._name + "has Bought " + pID + "\n\n"
            # print(toPrint)

class mMatrix:

    _size = 0

    users = []
    gID = None
    history = "**** SIMULATED GAME *******\n\n"

    def __init__(self, nOfPlayers=8):
        self._size = nOfPlayers

    def __str__(self):
        return self.history

    def allPing(self):
        for _player in self.users:
            _player.ping()

    def clearHist(self):
        self.allPing()
        for player in self.users:
            player.clearHistory()

    def incrementHistory(self, action):
        self.history += "**** %s ****\n\n" % (action)
        for player in self.users:
            self.history += player.__str__()
        self.history += "**** END OF %s ****\n" % (action)

    def lobby(self):
        for i in range(self._size):
            if i == 0:
                player = user("Hosty")
                player.host()
                self.gID = player.getGID()
                player.selectFigurine()
            else:
                player = user("Joiner" + str(i), "JOIN", self.gID)
                player.join()
                player.selectFigurine()
            self.users += [player]

        self.allPing()

        self.users[0].start()
        self.incrementHistory("LOBBY")

    def chat(self):
        self.clearHist()
        for _player in self.users:
            _player.chat()
        self.allPing()
        self.incrementHistory("CHAT")

    def roll(self):
        self.clearHist()
        for player in self.users:
            player.roll()
        self.allPing()
        self.incrementHistory("ROLL")

    def buy(self):
        self.clearHist()
        for player in self.users:
            player.buy()
        self.allPing()
        self.incrementHistory("BUY")

    def resetHistory(self, turn):
        self.history = "!!!!**** TURN %i *****!!!!!\n\n" % (turn)

    def simulate(self):
        self.lobby()
        #self.chat()
        turn = 0
        print(self.history)
        while True:
            turn += 1
            self.resetHistory(turn)
            self.roll()
            self.buy()
            print(self.history)

matrix = mMatrix(2)
matrix.simulate()
