class globalvar:

    def __init__(self):
        self.conversation_dict = {}

    def set_value(self, name, value):
        self.conversation_dict[name] = value
        return self

    def get_value(self, name, defValue=None):
        try:
            return self.conversation_dict[name]
        except KeyError:
            return defValue
