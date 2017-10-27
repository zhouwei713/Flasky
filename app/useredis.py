'''
Created on 2017415

@author: zhou
'''

import os
import redis
import time
from datetime import datetime
from config import config
from flask import current_app
rc = redis.Redis()

#cfg = config[os.getenv('FLASK_CONFIG') or 'default']()

def mark_online(user_id):
    now = int(time.time())
    #expires = now + (cfg.ONLINE_LAST_MINUTES * 60) + 10
    expires = now + (current_app.config['ONLINE_LAST_MINUTES'] * 60) + 10
    all_users_key = 'online-users/%d' % (now // 60)
    users_key = 'user-activity/%s' % user_id
    p = rc.pipeline()
    p.sadd(all_users_key, user_id)
    p.set(users_key, now)
    p.expireat(all_users_key, expires)
    p.expireat(users_key, expires)
    p.execute()

def get_user_last_activity(user_id):
    last_active = rc.get('user-activity/%s' % user_id)
    if last_active is None:
        return None
    return datetime.utcfromtimestamp(int(last_active))

def get_online_users():
    current = int(time.time()) // 60
    #minutes = xrange(cfg.ONLINE_LAST_MINUTES)
    minutes = xrange(current_app.config['ONLINE_LAST_MINUTES'])
    return rc.sunion(['online-users/%d' % (current - x) for x in minutes])


