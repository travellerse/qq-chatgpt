class Conversation:
    def __init__(self, ID):
        self.id = ID
        self.context = []

    def restart(self):
        self.context = []

    def add(self, text, name, op=0):
        if op == 0:
            text = str(name) + " : " + text
        self.context.append(text)

    def getParam(self):
        text = ""
        for i in self.context:
            text += i
        return text

    def getCount(self):
        num = 0
        for i in self.context:
            num += len(i)
        return num

    def clear(self):
        del self.context[0]
