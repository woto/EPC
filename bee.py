import redis
import json
import pdb
import sys

rs = redis.Redis('192.168.2.7')

ps = rs.pubsub()
ps.subscribe('bee')

#rc.publish('foo', 'hello world')

for item in ps.listen():
  #pdb.set_trace()
  data = json.loads(item['data'])
  print data
  print ''
  
  #if rs.setnx(data['data']['url'], 1):
  #  #print '1'
  #  rs.expire(data['data']['url'], 10)
  #else:
  #  print '2'