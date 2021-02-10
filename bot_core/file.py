# coding = utf-8
# author: holger version: 2.0
# license: AGPL-3.0
# belong: DailyReport-BotCore

import os
import re
import shutil
import stat
import sys
import webbrowser
import zipfile

import requests

from bot_core import exec_log, resources

# 运行目录
PROJECT_PATH = os.getcwd()

# 文件夹
DATA_FOLDER = 'data'
CMP_FOLDER = '.cmp_dat'

# 文件路径
CHROMEDRIVER_ZIP_FILE = os.path.join(PROJECT_PATH, DATA_FOLDER, 'chromedriver.zip')
CHROMEDRIVER_FILE = os.path.join(PROJECT_PATH, DATA_FOLDER,
                                 'chromedriver.exe' if sys.platform.lower().startswith('win32') else 'chromedriver')
USER_FILE = os.path.join(PROJECT_PATH, DATA_FOLDER, 'user.json')
MAPPING_FILE = os.path.join(PROJECT_PATH, DATA_FOLDER, 'mapping.json')
SCHEDULER_FILE = os.path.join(PROJECT_PATH, DATA_FOLDER, 'scheduler.json')
VERSION_FILE = os.path.join(PROJECT_PATH, DATA_FOLDER, 'version.json')
LOG_FILE = os.path.join(PROJECT_PATH, DATA_FOLDER, 'BotLog.log')

# 配置文件路径列表
FILE = [SCHEDULER_FILE, USER_FILE, MAPPING_FILE]

# 消息框路径
MSG_BOX_PATH = "https://api.holgerbest.top/msgbox.html?msg="

# 文件初始化
if not os.path.isdir(CMP_FOLDER):
    os.mkdir(CMP_FOLDER)
if not os.path.isdir(DATA_FOLDER):
    os.mkdir(DATA_FOLDER)
if not os.path.isfile(LOG_FILE):
    open(LOG_FILE, 'w', encoding='utf-8').close()


def get_file(filename: str) -> str:
    """
    配置文件选择器
    :param filename: user | mapping | scheduler | version
    :return: 配置文件路径
    """
    return {'user': USER_FILE, 'mapping': MAPPING_FILE,
            'scheduler': SCHEDULER_FILE, 'version': VERSION_FILE}[filename]


def get_cmp_file(file_path: str) -> str:
    """
    转换为比较文件路径
    :param file_path: 文件路径
    :return: 比较文件路径
    """
    return file_path.replace(DATA_FOLDER, CMP_FOLDER)


def copy_file(file_path=None) -> None:
    """
    复制文件到比较文件夹
    :param file_path: 原文件路径，为None复制全部配置文件
    :return: None
    """
    if file_path is None:
        for file in FILE:
            shutil.copyfile(file, get_cmp_file(file))
    else:
        assert file_path in FILE
        shutil.copyfile(file_path, get_cmp_file(file_path))


def same(old_data: dict, new_data: dict) -> bool:
    """
    比较两配置数据是否相同
    :param old_data: 旧配置数据
    :param new_data: 新配置数据
    :return: 是否相同
    """
    for key in old_data.keys():
        data = new_data.get(key)
        if isinstance(data, dict) and isinstance(old_data[key], dict) and not same(old_data[key], data):
            return False
        if old_data[key] != data:
            return False
    return True


def msg_box(desc: str) -> None:
    """
    以弹出页面的形式提醒用户
    :param desc: 提醒内容
    :return: None
    """
    webbrowser.open(MSG_BOX_PATH + desc)
    exec_log.logger(desc)


def chmod(path, mode) -> None:
    """
    Linux chmod 命令实现，修改文件权限
    :param path: 文件路径
    :param mode: 权限（数字）
    :return: None
    """
    RD, WD, XD = 4, 2, 1
    BNS = [RD, WD, XD]
    MDS = [
        [stat.S_IRUSR, stat.S_IRGRP, stat.S_IROTH],
        [stat.S_IWUSR, stat.S_IWGRP, stat.S_IWOTH],
        [stat.S_IXUSR, stat.S_IXGRP, stat.S_IXOTH]
    ]
    if isinstance(mode, int):
        mode = str(mode)
    if not re.match("^[0-7]{1,3}$", mode):
        raise Exception("mode does not conform to ^[0-7]{1,3}$ pattern")
    mode = "{0:0>3}".format(mode)
    mode_num = 0
    for midx, m in enumerate(mode):
        for bnidx, bn in enumerate(BNS):
            if (int(m) & bn) > 0:
                mode_num += MDS[bnidx][midx]
    os.chmod(path, mode_num)


def get_driver() -> None:
    """
    下载 Chrome 驱动程序
    :return: None
    """
    if sys.platform.startswith('linux'):
        chromedriver_url = 'https://chromedriver.storage.googleapis.com/87.0.4280.88/chromedriver_linux64.zip'
    elif sys.platform.startswith('win32'):
        chromedriver_url = 'https://chromedriver.storage.googleapis.com/87.0.4280.88/chromedriver_win32.zip'
    elif sys.platform.startswith('darwin'):
        chromedriver_url = 'https://chromedriver.storage.googleapis.com/87.0.4280.88/chromedriver_mac64.zip'
    else:
        msg_box(resources.ERR_UNSUPPORTED_PLATFORM)
        raise TypeError(resources.ERR_UNSUPPORTED_PLATFORM)

    with open(CHROMEDRIVER_ZIP_FILE, 'wb') as driver_zip:
        driver_zip.write(requests.get(chromedriver_url).content)

    with zipfile.ZipFile(CHROMEDRIVER_ZIP_FILE, 'r') as driver_zip:
        driver_zip.extractall(DATA_FOLDER)

    os.remove(CHROMEDRIVER_ZIP_FILE)
    chmod(path=CHROMEDRIVER_FILE, mode=777)
