import traceback

import requests

import config as cf


def getlabel(label):
    labels = {
        '0': "高",
        '1': "中",
        '2': "低"
    }
    return labels[label]


def send_msg(uid_or_gid, msg, msgid, is_private, label=None, size=None, time=None):
    if is_private == False:
        url = f"http://127.0.0.1:5700/send_group_msg?"
        message = f"[CQ:reply,id={msgid}] "+msg
    else:
        url = f"http://127.0.0.1:5700/send_private_msg?"
        message = msg

    if label is not None:
        message += (f"\n置信度：{getlabel(label)}")
    if size is not None:
        message += (f"\n对话容量：{str(size)}/{cf.get_value('Openai', 'max_size')}")
    if time is not None:
        message += (f"\n耗时：{str(time)}s")
    if is_private == False:
        data = {
            "group_id": uid_or_gid,
            "message": message
        }
    else:
        data = {
            "user_id": uid_or_gid,
            "message": message
        }

    try:
        requests.post(url, data=data, timeout=5)
    except Exception as e:
        error_print(e)
        pass


def error_print(error):
    info = str(error.args) + "\n==================\n" + \
        str(traceback.format_exc())
    print(info)
    return info
