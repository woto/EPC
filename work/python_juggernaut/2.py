import pdb
from juggernaut import Juggernaut
import redis

r = redis.Redis('192.168.2.3')
jug = Juggernaut(r)
pdb.set_trace()
for event, data in jug.subscribe_listen():
    print event
    if event == 'subscribe':
        print 'subscribe'
    elif event == 'unsubscribe':
        print 'unsubscribe'
    elif event == 'custom':
        print 'custom_event'