import os
import sys
import threading
import time
import traceback

import openai
from flask import Flask, request

import config as cf
from chat import chat

app = Flask(__name__)


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
        threading.Thread(target=chat, args=(
            gid, msg, msgid, json, False)).start()
        return "OK"

    return "OK"


def main():
    from gevent import pywsgi
    print(f"开始监听127.0.0.1:{int(cf.get_value('Openai', 'port'))}")
    server = pywsgi.WSGIServer(
        ('127.0.0.1', int(cf.get_value('Openai', 'port'))), app)
    server.serve_forever()


if __name__ == "__main__":
    main()
