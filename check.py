import config as cf
from api import send_group_msg, send_private_msg
from conversation import Conversation
from conversation import conversation_dict as con
from globalvar import globalvar

switch = globalvar()


def check_switch(uid_or_gid, msg, msgid, is_private):
    if msg.startswith('/switch'):
        if switch.get_value(uid_or_gid, False) == False:
            switch.set_value(uid_or_gid, True)
            msg = "已切换至Chatgpt3.5"
        else:
            switch.set_value(uid_or_gid, False)
            msg = "已切换至Chatgpt3.0"
        send_msg(uid_or_gid, msg, msgid, is_private)
        return switch.get_value(uid_or_gid), True
    return switch.get_value(uid_or_gid, False), False


def check(uid_or_gid, msg, msgid, is_private):

    if msg.startswith('/ls'):
        msg = con.get_all()
        send_msg(uid_or_gid, msg, msgid, is_private)
        return "OK"

    if msg.startswith('/init'):
        msg = msg.replace('/init', '').strip()
        if (con.get_value(uid_or_gid) == None):
            con.set_value(uid_or_gid, Conversation(uid_or_gid, is_private))
        con.set_value(uid_or_gid, con.get_value(uid_or_gid).setInit(msg))
        msg = '已初始化'
        send_msg(uid_or_gid, msg, msgid, is_private)
        return "OK"

    if msg.startswith('/param'):
        msg = f"""temperature = {con.get_value(uid_or_gid).getParam('temperature')}
top_p = {con.get_value(uid_or_gid).getParam('top_p')}
frequency_penalty = {con.get_value(uid_or_gid).getParam('frequency_penalty')}
presence_penalty = {con.get_value(uid_or_gid).getParam('presence_penalty')}"""
        send_msg(uid_or_gid, msg, msgid, is_private)
        return "OK"

    if msg.startswith('/context'):
        msg = con.get_value(uid_or_gid).getContext()
        send_msg(uid_or_gid, msg, msgid, is_private)
        return "OK"

    if msg.startswith('/re'):
        if (con.get_value(uid_or_gid) != None):
            con.set_value(uid_or_gid, con.get_value(uid_or_gid).restart())
            msg = '已清除对话'
            send_msg(uid_or_gid, msg, msgid, is_private,
                     size=con.get_value(uid_or_gid).getCount())
        return "OK"

    if msg.startswith('/help'):
        msg = help_text
        send_msg(uid_or_gid, msg, msgid, is_private)
        return "OK"

    if msg.startswith('/set'):
        msg = msg.replace('/set', '').strip()
        op, value = msg.split(' ')
        if op == 'temperature' or op == 't':
            if float(value) > 1 or float(value) < 0:
                send_msg(
                    uid_or_gid, f"超出范围，无法将temperature设置为{float(value)}", msgid, is_private)
                return "OK"
            con.set_value(uid_or_gid, con.get_value(
                uid_or_gid).setParam('temperature', float(value)))
            send_msg(
                uid_or_gid, f"将temperature设置为{float(value)}", msgid, is_private)
            return "OK"
        if op == 'top_p' or op == 'top':
            if float(value) > 1 or float(value) < 0:
                send_msg(
                    uid_or_gid, f"超出范围，无法将top_p设置为{float(value)}", msgid, is_private)
                return "OK"
            con.set_value(uid_or_gid, con.get_value(
                uid_or_gid).setParam('top_p', float(value)))
            send_msg(uid_or_gid, f"将top_p设置为{float(value)}", msgid, is_private)
            return "OK"
        if op == 'frequency_penalty' or op == 'f':
            if float(value) > 2 or float(value) < -2:
                send_msg(
                    uid_or_gid, f"超出范围，无法将frequency_penalty设置为{float(value)}", msgid, is_private)
                return "OK"
            con.set_value(uid_or_gid, con.get_value(
                uid_or_gid).setParam('frequency_penalty', float(value)))
            send_msg(
                uid_or_gid, f"将frequency_penalty设置为{float(value)}", msgid, is_private)
            return "OK"
        if op == 'presence_penalty' or op == 'p':
            if float(value) > 2 or float(value) < -2:
                send_msg(
                    uid_or_gid, f"超出范围，无法将presence_penalty设置为{float(value)}", msgid, is_private)
                return "OK"
            con.set_value(uid_or_gid, con.get_value(
                uid_or_gid).setParam('presence_penalty', float(value)))
            send_msg(
                uid_or_gid, f"将presence_penalty设置为{float(value)}", msgid, is_private)
            return "OK"


def send_msg(uid_or_gid, msg, msgid, is_private, label=None, size=None):
    if is_private == False:
        send_group_msg(uid_or_gid, msg, msgid, label, size)
    else:
        send_private_msg(uid_or_gid, msg, label, size)


help_text = """命令帮助
1. /set temperature(t) value
更高的值意味着模型将承担更多的风险。对于更有创意的应用程序，可以尝试0.9，对于有明确答案的应用程序，可以尝试0.0。
我们通常建议修改这个或top_p，但不建议同时修改。
value范围:0.0~1.0
2. /set top_p(top) value
温度采样的另一种替代方法称为核采样，其中模型考虑具有top_p概率质量的标记的结果。所以0.1意味着只考虑包含前10%概率质量的令牌。
我们通常建议改变这个或温度，但不建议两者都改变。
value范围:0.0~1.0
3. /set frequency_penalty(f) value
正值会根据新标记到目前为止是否出现在文本中来惩罚它们，从而增加模型谈论新主题的可能性。
value范围:-2.0~2.0
4. /set presence_penalty(p) value
正值会根据新符号在文本中的现有频率来惩罚它们，从而降低模型逐字重复同一行的可能性。
value范围:-2.0~2.0
5. /parameters(param)
显示现有参数。
6. /re
清除现有对话。
7. /init param
为模型初始化，param为模型的最初叙述，不会被/re清除。"""
