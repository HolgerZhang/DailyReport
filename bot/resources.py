# coding = utf-8
"""
file: bot/resources.py
author: holger
version: 3.0
license: AGPL-3.0
belongs: WebBot-BotCore
"""

import os
import re
import shutil
import stat
import sys
import webbrowser
import zipfile

import requests

from bot import exec_log
from bot.xml_parser import Resources

# 运行目录
RUNNING_PATH = os.getcwd()

# 包数据目录
PACKAGE_CFG_PATH = os.path.join(os.path.split(__file__)[0], 'BotCfg')

# 文件夹
DATA_FOLDER = 'data'
CMP_FOLDER = '.cmp_dat'

# 文件路径
CHROMEDRIVER_ZIP_FILE = os.path.join(PACKAGE_CFG_PATH, 'chromedriver.zip')
CHROMEDRIVER_FILE = os.path.join(PACKAGE_CFG_PATH,
                                 'chromedriver.exe' if sys.platform.lower().startswith('win32') else 'chromedriver')
CONFIGURATION_FILE = os.path.join(RUNNING_PATH, DATA_FOLDER, 'configuration.xml')
MAP_FILE = os.path.join(RUNNING_PATH, DATA_FOLDER, 'map.xml')
LOG_FILE = os.path.join(RUNNING_PATH, DATA_FOLDER, 'BotLog.log')
TEXT_SAVE_FILE = os.path.join(RUNNING_PATH, DATA_FOLDER, 'TextSaved.txt')

# 配置文件路径列表
FILE = [CONFIGURATION_FILE, MAP_FILE]

# 资源文件索引
R = Resources(os.path.join(PACKAGE_CFG_PATH, 'resource.xml'))

# 文件初始化
if not os.path.isdir(os.path.join(RUNNING_PATH, CMP_FOLDER)):
    os.mkdir(os.path.join(RUNNING_PATH, CMP_FOLDER))
if not os.path.isdir(os.path.join(RUNNING_PATH, DATA_FOLDER)):
    os.mkdir(os.path.join(RUNNING_PATH, DATA_FOLDER))
if not os.path.isdir(PACKAGE_CFG_PATH):
    os.mkdir(PACKAGE_CFG_PATH)
if not os.path.isfile(LOG_FILE):
    open(LOG_FILE, 'w', encoding='utf-8').close()
if not os.path.isfile(TEXT_SAVE_FILE):
    open(TEXT_SAVE_FILE, 'w', encoding='utf-8').close()


def get_file(filename: str) -> str:
    """
    文件选择器
    :param filename: config | map
    :return: 配置文件路径
    """
    return {'config': CONFIGURATION_FILE, 'map': MAP_FILE}[filename]


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


def msg_box(desc: str) -> None:
    """
    以弹出页面的形式提醒用户
    :param desc: 提醒内容
    :return: None
    """
    webbrowser.open(R.api.MSG_BOX_PATH + desc.replace("+", "%2B").replace("/", "%2F").replace(" ", "%20")
                    .replace("?", "%3F").replace("%", "%25").replace("#", "%23").replace("&", "%26")
                    .replace("=", "%3D").replace("\n", "%0A").replace("\t", "%09"))
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
        chromedriver_url = R.api.LINUX_CHROME_DRIVER.strip()
    elif sys.platform.startswith('win32'):
        chromedriver_url = R.api.WIN32_CHROME_DRIVER.strip()
    elif sys.platform.startswith('darwin'):
        chromedriver_url = R.api.MACOS_CHROME_DRIVER.strip()
    else:
        msg_box(R.string.ERR_UNSUPPORTED_PLATFORM)
        raise TypeError(R.string.ERR_UNSUPPORTED_PLATFORM)

    with open(CHROMEDRIVER_ZIP_FILE, 'wb') as driver_zip:
        driver_zip.write(requests.get(chromedriver_url).content)

    with zipfile.ZipFile(CHROMEDRIVER_ZIP_FILE, 'r') as driver_zip:
        driver_zip.extractall(PACKAGE_CFG_PATH)

    os.remove(CHROMEDRIVER_ZIP_FILE)
    chmod(path=CHROMEDRIVER_FILE, mode=777)
