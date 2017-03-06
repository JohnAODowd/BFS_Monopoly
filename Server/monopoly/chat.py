from monopoly.redisLib import getChat, setChat
from monopoly.helpers import getTime, keyStringtoInt

def addChat(gID, playerName, number, text):
    chat                    = getChat(gID)
    chat                    = keyStringtoInt(chat)
    thisChat                = {}
    thisChat["time"]        = getTime()
    thisChat["text"]        = text
    thisChat["playerName"]  = playerName
    thisChat["number"]      = number
    if len(chat) == 0:
        chat[0] = thisChat
    else:
        chat[max(chat) + 1] = thisChat
    setChat(gID, chat)