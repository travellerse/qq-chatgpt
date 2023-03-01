from revChatGPT.V1 import Chatbot

import config as cf
from globalvar import globalvar


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


chatbot_dict = globalvar()
