import requests


def getlabel(label):
    labels = {
        '0': "高",
        '1': "中",
        '2': "低"
    }
    return labels[label]


def send_private_msg(uid, msg, label=None, size=None):
    url = f"http://127.0.0.1:5700/send_private_msg?"
    message = msg
    if label is not None:
        message += ('\n置信度：'+getlabel(label))
    if label is not None:
        message += ('\n对话容量：'+str(size)+r"/1000")
    data = {
        "user_id": uid,
        "message": message
    }
    try:
        requests.post(url, data=data, timeout=5)
    except:
        pass


def send_group_msg(gid, msg, msgid, label=None, size=None):
    url = f"http://127.0.0.1:5700/send_group_msg?"
    message = f"[CQ:reply,id={msgid}] "+msg
    if label is not None:
        message += ('\n置信度：'+getlabel(label))
    if label is not None:
        message += ('\n对话容量：'+str(size)+r"/1000")
    data = {
        "group_id": gid,
        "message": message
    }
    try:
        requests.post(url, data=data, timeout=5)
    except:
        pass
