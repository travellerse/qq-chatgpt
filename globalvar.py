import conversation


def _init():
    global _global_dict
    _global_dict = {}


def set_value(name, value):
    _global_dict[name] = value
    print(name, value.getCount())


def get_value(name, defValue=None):
    try:
        return _global_dict[name]
    except KeyError:
        return defValue


def get_all():
    re = ""
    for i in _global_dict:
        c = _global_dict[i]
        re += "ID:"+str(c.id)+" 对话容量:"+str(c.getCount())+"/1000\n"
    return re
