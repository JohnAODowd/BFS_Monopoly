import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

games = r.getGames()
for gID in games:
    redis.set("players of " + gID)
    redis.delete("board of " + gID)
redis.set("games", "{}")
