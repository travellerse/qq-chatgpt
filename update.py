import os
import time
import requests
import zipfile

def check_update():
    with open("version.txt", "r") as f:
        version = f.read()
    # 请求服务器获取最新版本号
    response = requests.get(
        'https://github.com/travellerse/qq-chatgpt/raw/master/version.txt', verify=False)
    new_version = response.text

    # 判断本地版本号与服务器版本号是否一致
    if version != new_version:
        # 如果不一致，则下载最新版本的软件
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
    print('软件更新完成！\n请重新启动')
