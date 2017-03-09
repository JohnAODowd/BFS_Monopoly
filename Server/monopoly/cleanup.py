import redis
from monopoly import redisLib as rLib

r = redis.StrictRedis(host='213.32.22.158', port=6379, db=0)

games = rLib.getGames()
for gID in games:
    try:
        r.delete("players of " + gID)
    except:
        print ("players error")
    try:
        r.delete("board of " + gID)
    except:
        print ("board error")
    try:
        r.delete("deeds of " + gID)
    except:
        print ("deeds error")

r.set("games", "{}")