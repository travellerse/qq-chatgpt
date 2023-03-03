import configparser
import os


def _init():
    flag = configInit()
    global config  # 创建一个config对象
    config = configparser.RawConfigParser()
    config.read('config.yaml')  # 读取所有文件
    if flag:
        key = input("第一次运行，请输入Openai的APIkey\n")
        set_value('Openai', "APIkey", key)


def configInit():
    if not os.path.exists('config.yaml'):
        with open('config.yaml', 'w') as f:
            f.write(configfile)
        return True
    else:
        return False


def get_value(section, name):  # 获取某个文件中的某个变量
    if section == 'Parameter':
        return float(config.get(section, name))
    return config.get(section, name)


def set_value(section, name, value):  # 修改某个文件中的某个变量
    config.set(section, name, str(value))
    with open('config.yaml', 'w') as f:
        config.write(f)


configfile = """[Openai]
APIkey = 
port = 9000

[Chatgpt]
email =
password =
proxy = http://127.0.0.1:7890
access_token = 
"""
