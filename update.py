import os
import time
import requests
import zipfile
import re


def compare_version(v1, v2):
    """
    :return: 如果v1>v2，返回1；如果v1=v2，返回0；如果v1<v2，返回-1
    """
    # 通过正则表达式将版本号分割成列表
    v1_list = re.split(r'[.-]', v1[1:])
    v2_list = re.split(r'[.-]', v2[1:])

    # 比较版本号列表的每一项，如果当前项不相同，则返回比较结果
    for i in range(min(len(v1_list), len(v2_list))):
        if v1_list[i] != v2_list[i]:
            if int(v1_list[i]) > int(v2_list[i]):
                return 1
            else:
                return -1

    if (len(v1_list) != len(v2_list)):
        return -1 if len(v1_list) > len(v2_list) else 1
    # 如果所有项都相同，则返回0
    return 0


def check_update():
    with open("version.txt", "r") as f:
        version = f.read()
    # 请求服务器获取最新版本号
    try:
        response = requests.get(
            'https://github.com/travellerse/qq-chatgpt/raw/master/version.txt')
    except:
        response = requests.get(
            'https://github.com/travellerse/qq-chatgpt/raw/master/version.txt', verify=False)
    new_version = response.text

    # 判断本地版本号与服务器版本号
    if compare_version(version, new_version) == -1:
        download_update(new_version)
        return True
    else:
        # 如果一致，则不用更新
        print('您的软件已是最新版本！')
        return False


# 定义下载更新的函数
def download_update(version):
    # 下载最新版本的软件
    filename = 'qq-chatgpt-'+version+'.zip'
    try:
        response = requests.get(
            'https://github.com/travellerse/qq-chatgpt/releases/download/'+version+'/'+'qq-chatgpt-'+version+'.zip')
    except:
        response = requests.get(
            'https://github.com/travellerse/qq-chatgpt/releases/download/'+version+'/'+'qq-chatgpt-'+version+'.zip', verify=False)
    with open(filename, 'wb') as f:
        f.write(response.content)

    # 解压文件
    zip_file = zipfile.ZipFile(filename, 'r')
    zip_file.extractall('./')
    zip_file.close()

    # 删除压缩文件
    os.remove(filename)

    # 提示更新完成
    print('软件更新完成！\n将重新启动')
