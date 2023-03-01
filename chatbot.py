from revChatGPT.V1 import Chatbot
import config as cf


class chatbot:

    def __init__(self, ID):
        self.id = ID
        try:
            self.core = Chatbot(config={
                "email": cf.get_value("Chatgpt", "email"),
                "password": cf.get_value("Chatgpt", "password"),
                "proxy": cf.get_value("Chatgpt", "proxy")}
            )
        except:
            self.core = Chatbot(config={
                "access_token": cf.get_value("Chatgpt", "access_token"),
                "proxy": cf.get_value("Chatgpt", "proxy")}
            )


def _init():
    global conversation_dict
    conversation_dict = {}


def set_value(name, value):
    conversation_dict[name] = value


def get_value(name, defValue=None):
    try:
        return conversation_dict[name]
    except KeyError:
        return defValue
