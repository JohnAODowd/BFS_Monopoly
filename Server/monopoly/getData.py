import requests
from json import loads
from monopoly.helpers import keyStringtoInt

url = "http://213.32.22.158/"

def getBoardJson():
    response = requests.get(url + "board.json")
    board = keyStringtoInt(loads(response.text)["board"])
    return board

def getChanceJson():
    response = requests.get(url + "cards.json")
    return loads(response.text)["cards"]['Chance']

def getCommChestJson():
    response = requests.get(url + "cards.json")
    return loads(response.text)["cards"]['CommunityChest']

def getPropertiesJson():
    response = requests.get(url + "properties.json")
    return loads(response.text)

def getInitJson():
    response = requests.get(url + "init.json")
    return loads(response.text)

def getFigurinesJson():
    response = requests.get(url + "figurines.json")
    return loads(response.text)['figurines']