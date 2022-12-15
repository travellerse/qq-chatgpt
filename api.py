import requests


def getlabel(label):
    labels = {
        '0': "高",
        '1': "中",
        '2': "低"
    }
    return labels[label]


def send_private_msg(uid, msg, label):
    url = f"http://127.0.0.1:5700/send_private_msg?"
    data = {
        "user_id": uid,
        "message": msg+'\n置信度：'+getlabel(label)
    }
    try:
        requests.post(url, data=data, timeout=5)
    except:
        pass


def send_group_msg(gid, msg, msgid, label=None):
    url = f"http://127.0.0.1:5700/send_group_msg?"
    message = f"[CQ:reply,id={msgid}] "+msg
    if label is not None:
        message += ('\n置信度：'+getlabel(label))
    data = {
        "group_id": gid,
        "message": message
    }
    try:
        requests.post(url, data=data, timeout=5)
    except:
        pass
