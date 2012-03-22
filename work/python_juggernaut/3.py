import redis
rc = redis.Redis()

ps = rc.pubsub()
ps.subscribe(['chat', 'juggernaut'])

rc.publish('foo', 'hello world')

for item in ps.listen():
    if item['type'] == 'message':
        print item['channel']
        print item['data']
