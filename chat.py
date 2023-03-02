from time import time

import config as cf
from api import error_print, send_msg
from chatbot import chatbot
from chatbot import chatbot_dict as bot
from chatgpt import getResponse
from check import check, check_switch
from conversation import Conversation
from conversation import conversation_dict as con


def chat(uid_or_gid, msg, msgid, json, is_private):
    start = time()
    chatgpt, flag = check_switch(uid_or_gid, msg, msgid, is_private)
    if (flag == True):
        return "OK"
    if (chatgpt == False):
        if con.get_value(uid_or_gid) == None:
            con.set_value(uid_or_gid, Conversation(uid_or_gid, is_private))
        if check(uid_or_gid, msg, msgid, is_private) == "OK":
            return "OK"
        con.set_value(uid_or_gid, con.get_value(uid_or_gid).add(msg, "user"))
        while con.get_value(uid_or_gid).getCount() > int(cf.get_value('Openai', 'max_size')):
            con.set_value(uid_or_gid, con.get_value(uid_or_gid).clear())
        try:
            re, role = getResponse(con.get_value(
                uid_or_gid).getContext()+"\nassistant:", uid_or_gid)
            con.set_value(uid_or_gid, con.get_value(uid_or_gid).add(re, role))
            while con.get_value(uid_or_gid).getCount() > int(cf.get_value('Openai', 'max_size')):
                con.set_value(uid_or_gid, con.get_value(uid_or_gid).clear())
        except Exception as e:
            re = error_print(e)
            con.set_value(uid_or_gid, con.get_value(uid_or_gid).restart())
        end = time()
        send_msg(uid_or_gid, re, msgid, is_private, None,
                 con.get_value(uid_or_gid).getCount(), time='{:.3f}'.format(end-start))

    else:
        try:
            re = getResponse(msg, uid_or_gid, True)
        except Exception as e:
            re = error_print(e)
        end = time()
        send_msg(uid_or_gid, re, msgid, is_private,
                 time='{:.3f}'.format(end-start))
