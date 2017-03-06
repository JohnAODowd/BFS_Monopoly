import requests
from json import loads
from monopoly.helpers import keyStringtoInt

url = "http://hassassin.netsoc.co/monopolyJSON/"

def getBoardJson():
    response = requests.get(url + "board.json")
    board = keyStringtoInt(loads(response.text)["board"])
    return board

def getChanceJson():
    response = requests.get(url + "chance.json")
    return loads(response.text)['Chance']

def getCommChestJson():
    response = requests.get(url + "commchest.json")
    return loads(response.text)['CommunityChest']

def getPropertiesJson():
    response = requests.get(url + "properties.json")
    return loads(response.text)

def getInitJson():
    response = requests.get(url + "init.json")
    return loads(response.text)

def getFigurinesJson():
    response = requests.get(url + "figurines.json")
    return loads(response.text)['figurines']