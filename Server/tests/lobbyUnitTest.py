import json
import requests


def post(d):
	js = d
	payload = json.dumps(js)
	headers = {'Content-Type' : 'application/json'}
	r = requests.post("http://leela.netsoc.co:8080/game", data=payload, headers=headers)
	return r.text

class user:

    _gID        = None
    _uID        = None
    _figurine   = None
    _name       = None
    _figurines  = None
    _history    = None
    _type       = "HOST"
    _option     = None

    def __init__(self, name, type="HOST", gID=None):
        self._name      = name
        self._history   = "Request history: ***************************\n\n"
        if type != "HOST":
            self._gID   = gID
            self._type  = "JOIN"

    def __str__(self):
        string = "Name: " + self._name + "\n"
        string += "gID: " + self._gID + "\n"
        string += "uID: " + self._uID + "\n"
        string += "figurine: " + self._figurine + "\n"
        string += "\n" + self._history
        string += "\n*****************************"
        return string

    def host(self):
        js                  = {}
        js["request"]       = "HOST"
        js["name"]          = self._name
        js["type"]          = "private"
        self._history       += "SENDING (HOST)*****\n" + str(js) + "\n\n"
        response            = post(js)
        self._history       += "RECIEVED***********\n" + response + "\n\n"
        response            = json.loads(response)
        self._gID           = response["game"]["gID"]
        self._uID           = response["player"]["uID"]
        self._figurines     = response['game']['figurines']

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
            self._uID           = response["player"]["uID"]
            self._figurines     = response['game']['figurines']

    def selectFigurine(self):
        if self._figurines != None and len(self._figurines) > 0:
            figurine            = self._figurines[0]
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

    def getGID(self):
        return self._gID

    def ping(self):
        js                  = {}
        js["request"]       = "PING"
        js["uID"]           = self._uID
        js["gID"]           = self._gID
        self._history       += "SENDING (PING)*\n" + str(js) + "\n\n"
        response            = post(js)
        self._history       += "RECIEVED***********\n" + response + "\n\n"
        if self._type == "HOST":
            response    = json.loads(response)
            if "START" in response["options"]:
                self._option = "START"

    def start(self):
        js = {}
        js["request"] = "START"
        js["uID"] = self._uID
        js["gID"] = self._gID
        self._history += "SENDING (START)*\n" + str(js) + "\n\n"
        response = post(js)
        self._history += "RECIEVED***********\n" + response + "\n\n"

def test():
    users   = []
    gID     = None
    for i in range(8):
        player = None
        if i == 0:
            player  = user("Hosty")
            player.host()
            gID     = player.getGID()
            player.selectFigurine()
        else:
            player  = user("Joiner" + str(i), "JOIN", gID)
            player.join()
            player.selectFigurine()
        users += [player]

    for _player in users:
        _player.ping()

    users[0].start()

    for _player in users:
        print(_player)



test()