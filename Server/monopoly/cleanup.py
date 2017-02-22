import redis
from monopoly import redisLib as rLib

r = redis.StrictRedis(host='localhost', port=6379, db=0, password="Glad0s7334")

games = rLib.getGames()
for gID in games:
    r.delete("players of " + gID)
    r.delete("board of " + gID)
r.set("games", "{}")
