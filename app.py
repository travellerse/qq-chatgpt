from flask import Flask, request
from api import send_private_msg
from api import send_group_msg
from chatgpt import getResponse
from update import check_update
import globalvar as gl
app = Flask(__name__)


@app.route('/', methods=["POST", "GET"])
def get_data():
    if request.get_json().get('message_type') == 'private':
        uid = request.get_json().get('sender').get('user_id')
        msg = request.get_json().get('raw_message')
        msgid = request.get_json().get('message_id')
        re, label = getResponse(msg)
        send_private_msg(uid, re, label)

    if request.get_json().get('message_type') == 'group' and request.get_json().get('raw_message').startswith('[CQ:at,qq=3550491050]'):
        gid = request.get_json().get('group_id')
        uid = request.get_json().get('sender').get('user_id')
        msg = request.get_json().get('raw_message').replace(
            '[CQ:at,qq=3550491050]', '').strip()
        msgid = request.get_json().get('message_id')

        if msg.startswith('/param'):
            msg = f"""temperature = {gl.get_value('Parameter','temperature')}
top_p = {gl.get_value('Parameter','top_p')}
frequency_penalty = {gl.get_value('Parameter','frequency_penalty')}
presence_penalty = {gl.get_value('Parameter','presence_penalty')}"""
            send_group_msg(gid, msg, msgid)
            return "OK"

        if msg.startswith('/help'):
            msg = """调参命令帮助
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
显示现有参数"""
            send_group_msg(gid, msg, msgid)
            return "OK"

        if msg.startswith('/set'):
            msg = msg.replace('/set', '').strip()
            op, value = msg.split(' ')
            if op == 'temperature' or op == 't':
                if float(value) > 1 or float(value) < 0:
                    send_group_msg(
                        gid, f"超出范围，无法将temperature设置为{float(value)}", msgid)
                    return "OK"
                gl.set_value('Parameter', 'temperature', float(value))
                send_group_msg(gid, f"将temperature设置为{float(value)}", msgid)
                return "OK"
            if op == 'top_p' or op == 'top':
                if float(value) > 1 or float(value) < 0:
                    send_group_msg(
                        gid, f"超出范围，无法将top_p设置为{float(value)}", msgid)
                    return "OK"
                gl.set_value('Parameter', 'top_p', float(value))
                send_group_msg(gid, f"将top_p设置为{float(value)}", msgid)
                return "OK"
            if op == 'frequency_penalty' or op == 'f':
                if float(value) > 2 or float(value) < -2:
                    send_group_msg(
                        gid, f"超出范围，无法将frequency_penalty设置为{float(value)}", msgid)
                    return "OK"
                gl.set_value('Parameter', 'frequency_penalty', float(value))
                send_group_msg(
                    gid, f"将frequency_penalty设置为{float(value)}", msgid)
                return "OK"
            if op == 'presence_penalty' or op == 'p':
                if float(value) > 2 or float(value) < -2:
                    send_group_msg(
                        gid, f"超出范围，无法将presence_penalty设置为{float(value)}", msgid)
                    return "OK"
                gl.set_value('Parameter', 'presence_penalty', float(value))
                send_group_msg(
                    gid, f"将presence_penalty设置为{float(value)}", msgid)
                return "OK"

        re, label = getResponse(msg)
        send_group_msg(gid, re, msgid, label)

    return "OK"


def main():
    #check_update()
    from gevent import pywsgi
    server = pywsgi.WSGIServer(('127.0.0.1', 9000), app)
    server.serve_forever()


main()
