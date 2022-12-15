import configparser
import os


def _init():
    configInit()
    global config  # 创建一个config对象
    config = configparser.ConfigParser()
    config.read('config.yaml')  # 读取所有文件


def configInit():
    if not os.path.exists('config.yaml'):
        with open('config.yaml', 'w') as f:
            f.write(configfile)
    key = input("第一次运行，请输入Openai的APIkey")
    set_value('Openai', "APIkey", key)


def get_value(section, name):  # 获取某个文件中的某个变量
    if section == 'Parameter':
        return float(config.get(section, name))
    return config.get(section, name)


def set_value(section, name, value):  # 修改某个文件中的某个变量
    config.set(section, name, str(value))
    with open('config.yaml', 'w') as f:
        config.write(f)


configfile = """[Openai]
APIkey : 

[Parameter]
temperature : 0
top_p : 1
frequency_penalty : 0
presence_penalty : 0
"""
