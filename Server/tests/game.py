class game:

    _trade      = {}
    _turn       = None
    _figurines  = None
    _gID        = None
    _buildings  = None
    _lastRoll   = None
    _state      = None

    def __init__(self, dic):
        self._figurines = dic["figurines"]
        self._state     = dic["state"]
        self._gID       = dic['gID']

    def update(self, dic):
        if self._trade != dic["trade"]:
            self._trade = dic["trade"]

        if self._turn != dic["turn"]:
            self._turn = dic["turn"]

        if self._buildings != dic["buildings"]:
            self._buildings = dic["buildings"]

        if self._figurines != dic["figurines"]:
            self._figurines = dic["figurines"]

        if self._lastRoll != dic["lastRoll"]:
            self._lastRoll = dic["lastRoll"]

        if self._state != dic["state"]:
            self._state = dic["state"]

    def getTrade(self):
        return self._trade

    def getTurn(self):
        return self._turn

    def getFigurines(self):
        return self._figurines

    def getGID(self):
        return self._gID

    def getBuildings(self):
        return self._buildings

    def getState(self):
        return self._state

class options:

    _lst = []

    def __init__(self, lst):
        self._lst = lst

    def update(self, lst):
        if self._lst != lst:
            self._lst = lst
            return True

    def getOptions(self):
        return self._lst

class player:

    _uID        = None
    _money      = 0
    _GOOJF      = {}
    _jail       = {}
    _pos        = 0
    _name       = ""
    _figurine   = None
    _properties = {}
    _number     = 0
    _trade      = {}
    _pID        = None

    def __init__(self, dic):
        self._uID           = dic["uID"]
        self._money         = dic["money"]
        self._GOOJF         = dic["public"]["GOOJF"]
        self._jail          = dic["public"]["jail"]
        self._pos           = dic["public"]["position"]
        self._name          = dic["public"]["name"]
        self._number        = dic["public"]["number"]
        self._properties    = dic["public"]["properties"]

    def update(self, dic):
        self._money = dic["money"]
        self._GOOJF = dic["public"]["GOOJF"]
        self._jail = dic["public"]["jail"]
        self._pos = dic["public"]["position"]
        self._figurine = dic["public"]["figurine"]
        self._properties = dic["public"]["properties"]
        if dic["canBuy"] != None:
            self._pID = dic["canBuy"]
        else:
            self._pID = None

class Game:

    _game       = None
    _player     = None
    _options    = None

    def __init__(self, dic):
        self._game      = game(dic["game"])
        self._player    = player(dic["player"])
        self._options   = dic["options"]

    def update(self, dic):
        self._game.update(dic["game"])
        self._player.update(dic["player"])
        self._options = dic["options"]
        print(self._options)

    def game(self):
        return self._game

    def player(self):
        return self._player

    def options(self):
        return self._options