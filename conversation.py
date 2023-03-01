from globalvar import globalvar


class Conversation:

    def __init__(self, ID, Is_private):
        self.id = ID
        self.is_private = Is_private
        self.init = ""
        self.context = [self.init]
        self.temperature = 0.5
        self.top_p = 0
        self.frequency_penalty = 0
        self.presence_penalty = 0

    def setInit(self, text):
        self.init = text
        self.context = [self.init]
        return self

    def restart(self):
        self.context = [self.init]
        return self

    def add(self, text, name=None):
        if name is not None:
            text = str(name) + ":" + text
        self.context.append(text)
        return self

    def getContext(self):
        return "\n".join(self.context)

    def getCount(self):
        return sum(len(i) for i in self.context)

    def clear(self):
        self.context.pop(1)
        return self

    def setParam(self, op, value):
        if op == 'temperature':
            self.temperature = value
            return self
        if op == 'top_p':
            self.top_p = value
            return self
        if op == 'frequency_penalty':
            self.frequency_penalty = value
            return self
        if op == 'presence_penalty':
            self.presence_penalty = value
            return self

    def getParam(self, op):
        if op == 'temperature':
            return self.temperature
        if op == 'top_p':
            return self.top_p
        if op == 'frequency_penalty':
            return self.frequency_penalty
        if op == 'presence_penalty':
            return self.presence_penalty


class globalvar_converstaion(globalvar):
    def __init__(self):
        globalvar.__init__(self)

    def get_all(self):
        re = ""
        for i in self.conversation_dict:
            c = self.conversation_dict[i]
            re += "ID:"+str(c.id)+" 对话容量:"+str(c.getCount())+"/1000\n"
        return re


conversation_dict = globalvar_converstaion()
