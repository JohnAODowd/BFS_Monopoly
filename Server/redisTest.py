import redis
r = redis.StrictRedis(host='213.32.22.158', port=6379, db=0)

r.set("ping", "pong")
print(r.ping())