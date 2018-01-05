'''
Created on 20171025

@author: zhou
'''

from flask import Flask, request, session, render_template, Response, jsonify, redirect, flash, url_for
from . import chat
import redis
import time
import json
import config
import gevent
from .models import Comet, rm_channel_placeholder
from .text import linkify, escape_text
from ..api.onlineusers import mark_online, get_online_users, get_user_last_activity

rc = redis.Redis()

@chat.before_app_request
def mark_current_user_online():
    if request.headers.get('X-Forwarded-For'):
        mark_online(request.headers['X-Forwarded-For'])
    else:
        mark_online(request.remote_addr)

@chat.route('/chat/test')
def chat_test():
    return render_template('chat/test.html')

@chat.route('/chat/item1')
def chat_item1():
    return render_template('chat/item-1.html')

@chat.route('/chat/index', methods=['GET', 'POST'])
def chat_index():
    t = time.asctime( time.localtime(time.time()) )
    Online_user = get_online_users()
    return render_template('chat/index_chat.html',Online_user=Online_user, t=t)

'''
def is_admin():
    if session.get('admin'):
        return True
    return False

def is_duplicate_name():
    user_name = session.get('user', '')
    for online_user in rc.zrange(config.ONLINE_USER_CHANNEL,0,-1):
        if online_user == user_name.encode('utf-8'):
            flash(u'This user name not available, please change another one')
            session.pop('user', None)
            return True
        return False
'''
def rm_channel_placeholder(data):
    for index, item in enumerate(data):
        if item == config.CHANNEL_PLACEHOLDER:
            data.pop(index)
'''

@chat.route('/chat/admin')
def admin():
    session['admin'] = 1
    return redirect(url_for('.chat_home'))

@chat.route('/chat')
def chat_index():
    if session.get('user'):
        return redirect('/chat/home')
    return render_template('chat/chat_index.html')

@chat.route('/chat/change_name')
def chat_chg_name():
    session.pop('user', None)
    return redirect(url_for('.chat_index'))

@chat.route('/chat/login', methods=['POST'])
def chat_login():
    user_name = request.form.get('user_name','')
    session['user'] = user_name
    if is_duplicate_name():
        return redirect(url_for('.chat_index'))
    return redirect(url_for('.chat_home'))


@chat.route('/chat/home', methods=['GET','POST'])
def chat_home():
    if not session.get('user'):
        return redirect(url_for('.chat_index'))

    if request.method == 'POST':
        title = request.form.get('title','')
        if not title:
            return jsonify(status='error',message={'title': 'empty title'})

        room_id = rc.incr(config.ROOM_INCR_KEY)
        rc.set(config.ROOM_INFO_KEY.format(room=room_id),
               json.dumps({'title':title,'room_id':room_id,'user':session['user'],'created':time.time()})
               )
        return redirect('/chat/room')
    rooms=[]
    room_info_keys = config.ROOM_INFO_KEY.format(room='*')
    for room_info_key in rc.keys(room_info_keys):
        room_info = json.loads(rc.get(room_info_key))
        users = rc.zrevrange(config.ROOM_ONLINE_USER_CHANNEL.format(room=room_info['room_id']),0,-1)
        rm_channel_placeholder(users)
        rooms.append({
            'id':room_info['room_id'],
            'creator':room_info['user'],
            'content':map(json.loads, reversed(rc.zrevrange(config.ROOM_CHANNEL.format(room=room_info['room_id']),0,4))),
            'title':room_info['title'],
            'users':users,
        })
    return render_template('chat/chat.html', rooms=rooms, uri=request.path, is_admin=is_admin())

@chat.route('/chat/rm_room', methods=['POST'])
def chat_rm_room():
    if not session.get('user'):
        return redirect('/chat')
    room_id = request.form.get('room_id')
    room_key = config.ROOM_INFO_KEY.format(room=room_id)
    romm_channel = config.ROOM_CHANNEL.format(room=room_id)
    room = json.loads(rc.get(room_key))
    if not is_admin():
        return jsonify(status='error',content={'message':'permission denied'})
    rc.delete(room_key)
    rc.delete(romm_channel)
    return jsonify(status='ok', content={'url':'/chat'})

@chat.route('/chat/<int:room_id>')
def chat_room(room_id):
    if not session.get('user'):
        return redirect(url_for('.chat_index'))
    user_name = session['user']
    room = json.loads(rc.get(config.ROOM_INFO_KEY.format(room=room_id)))
    room_online_user_channel = config.ROOM_ONLINE_USER_CHANNEL.format(room=room_id)
    room_online_user_signal = config.ROOM_ONLINE_USER_SIGNAL.format(room=room_id)

    rc.zadd(config.ONLINE_USER_CHANNEL, user_name, time.time())
    rc.zadd(room_online_user_channel, user_name, time.time())
    rc.publish(config.ONLINE_USER_SIGNAL, '')
    rc.publish(room_online_user_signal, json.dumps({'room_id':room_id}))

    room_content = reversed(rc.zrevrange(config.ROOM_CHANNEL.format(room=room_id), 0, 200, withscores=True))
    room_content_list = []
    for item in room_content:
        room_content_list.append(json.loads(item[0]))

    room_online_users = []
    for user in rc.zrange(room_online_user_channel,0,-1):
        if user == config.CHANNEL_PLACEHOLDER:
            continue
        room_online_users.append(user.decode('utf-8'))

    return render_template('chat/room.html',
                           room_content = room_content_list,
                           uri = request.path,
                           room_name = room['title'],
                           room_id = room_id,
                           room_online_users = room_online_users
                           )
@chat.route('/chat/post_content', methods=['POST'])
def chat_post_content():
    if not session.get('user'):
        return redirect('/chat')

    room_id = request.form.get('room_id')
    data = {'user': session.get('user'),
            'content': linkify(escape_text(request.form.get('content', ''))),
            'created': time.strftime('%m-%d %H:%M:%S'),
            'room_id': room_id,
            'id': rc.incr(config.ROOM_CONTENT_INCR_KEY),
            }
    rc.zadd(config.ROOM_CHANNEL.format(room=room_id), json.dumps(data), time.time())
    return jsonify(**data)

@chat.route('/chat/comet')
def chat_comet():
    uri = request.args.get('uri','')
    room_id = request.args.get('room_id','')
    comet = request.args.get('comet','').split(',')
    ts = request.args.get('ts',time.time())
    channel = config.CONN_CHANNEL_SET.format(channel=request.args.get('channel'))

    cmt = Comet()
    result = cmt.check(channel, comet, ts, room_id)
    if result:
        return jsonify(**result)

    passed_time = 0
    while passed_time < config.COMET_TIMEOUT:
        comet = rc.smembers(config.CONN_CHANNEL_SET.format(channel=channel))
        result = cmt.check(channel, comet, ts, room_id)
        if result:
            return jsonify(**result)
        passed_time += config.COMET_POLL_TIME
        gevent.sleep(config.COMET_POLL_TIME)

    if room_id:
        room_online_user_channel = config.ROOM_ONLINE_USER_CHANNEL.format(room=room_id)
        rc.zadd(room_online_user_channel, session['user'], time.time())
    rc.zadd(config.ONLINE_USER_CHANNEL, session['user'], time.time())

    return jsonify(ts=time.time())
    
'''









