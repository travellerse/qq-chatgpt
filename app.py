import os
import sys
import threading

import openai
from flask import Flask, request

import config as cf
import globalvar as gl
from api import send_group_msg, send_private_msg
from chatgpt import getResponse
from check import check
from conversation import Conversation
from update import check_update

app = Flask(__name__)

lock = threading.Lock()


def chat(uid_or_gid, msg, msgid, json, is_private=False):
    # lock.acquire()
    if gl.get_value(uid_or_gid) == None:
        gl.set_value(uid_or_gid, Conversation(uid_or_gid, is_private))
    if check(uid_or_gid, msg, msgid, is_private) == "OK":
        return "OK"
    gl.set_value(uid_or_gid, gl.get_value(uid_or_gid).add(msg, "user"))
    while gl.get_value(uid_or_gid).getCount() > 1000:
        gl.set_value(uid_or_gid, gl.get_value(uid_or_gid).clear())
    try:
        re, label = getResponse(gl.get_value(
            uid_or_gid).getContext()+"\nAI:", uid_or_gid)
        gl.set_value(uid_or_gid, gl.get_value(uid_or_gid).add(re, "AI"))
        while gl.get_value(uid_or_gid).getCount() > 1000:
            gl.set_value(uid_or_gid, gl.get_value(uid_or_gid).clear())
    except Exception as e:
        re = e, label = None
        gl.set_value(uid_or_gid, gl.get_value(uid_or_gid).restart())

    if is_private:
        send_private_msg(uid_or_gid, re, label,
                         gl.get_value(uid_or_gid).getCount())
    else:
        msgid = json.get('message_id')
        send_group_msg(uid_or_gid, re, msgid, label,
                       gl.get_value(uid_or_gid).getCount())
    # lock.release()


@app.route('/', methods=["POST", "GET"])
def get_data():
    json = request.get_json()
    if json.get('message_type') == 'private':
        uid = json.get('sender').get('user_id')
        msg = json.get('raw_message')
        msgid = json.get('message_id')
        threading.Thread(target=chat, args=(
            uid, msg, msgid, json, True)).start()
        return "OK"

    if json.get('message_type') == 'group' and json.get('raw_message').startswith('[CQ:at,qq=3550491050]'):
        gid = json.get('group_id')
        msg = json.get('raw_message').replace(
            '[CQ:at,qq=3550491050]', '').strip()
        msgid = json.get('message_id')
        threading.Thread(target=chat, args=(gid, msg, msgid, json)).start()
        return "OK"

    return "OK"


def main():
    gl._init()
    from gevent import pywsgi
    print(f"开始监听127.0.0.1:{int(cf.get_value('Openai', 'port'))}")
    server = pywsgi.WSGIServer(
        ('127.0.0.1', int(cf.get_value('Openai', 'port'))), app)
    server.serve_forever()


main()
