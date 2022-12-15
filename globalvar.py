def _init():
    global _global_dict
    _global_dict = {}


def set_value(name, value):
    _global_dict[name] = value


def get_value(name, defValue=None):
    try:
        return _global_dict[name]
    except KeyError:
        return defValue

import requests

url = "https://api.newnative.ai/stable-diffusion?prompt=futuristic spce station, 4k digital art"

response = requests.request("GET", url)
data = response.json()
print(data["image_url"])