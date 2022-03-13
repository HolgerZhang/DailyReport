# coding = utf-8
# author: holger
# version: 4.0.0
# license: AGPL-3.0
# belong: DailyReport-BotCore

import os
import platform
import re
import shutil
import stat
import sys
import zipfile

import requests

from BotCore import logger

# 运行目录
PROJECT_PATH = os.getcwd()

# 文件夹
DATA_FOLDER = 'data'
MAIL_FOLDER = 'mail'

# 文件路径
MAPPING_FILE = os.path.join(PROJECT_PATH, DATA_FOLDER, 'mapping.json')
VERSION_FILE = os.path.join(PROJECT_PATH, DATA_FOLDER, 'version.json')
SUCCESS_MAIL_FILE = os.path.join(PROJECT_PATH, DATA_FOLDER, MAIL_FOLDER, 'success-template.html')
FAIL_MAIL_FILE = os.path.join(PROJECT_PATH, DATA_FOLDER, MAIL_FOLDER, 'fail-template.html')
DEFAULT_DRIVER_PATH = os.path.join(PROJECT_PATH, DATA_FOLDER,
                                   'driver.exe' if sys.platform.lower().startswith('win32') else 'driver')

# NO_GUI = os.environ.get('BOT_CORE_NO_GUI', 'FALSE').upper() == 'TRUE'

# 文件初始化
if not os.path.isdir(DATA_FOLDER):
    os.mkdir(DATA_FOLDER)


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


def mv(src, dst):
    if not os.path.isfile(src):
        print("%s not exist!" % src)
    else:
        path, name = os.path.split(dst)  # 分离文件名和路径
        if not os.path.exists(path):
            os.makedirs(path)  # 创建路径
        shutil.move(src, dst)  # 移动文件
        print("move %s -> %s" % (src, dst))


def get_chrome_driver(path) -> None:
    """
    下载 Chrome 驱动程序
    :return: None
    """
    CHROMEDRIVER_ZIP_FILE = os.path.join(PROJECT_PATH, DATA_FOLDER, 'chromedriver.zip')
    CHROMEDRIVER_FILE = os.path.join(PROJECT_PATH, DATA_FOLDER,
                                     'chromedriver.exe' if sys.platform.lower().startswith('win32') else 'chromedriver')
    chrome_version = str(requests.get('https://chromedriver.storage.googleapis.com/LATEST_RELEASE').text)
    if sys.platform.startswith('linux'):
        chromedriver_url = 'https://chromedriver.storage.googleapis.com/' + chrome_version + '/chromedriver_linux64.zip'
    elif sys.platform.startswith('win32'):
        chromedriver_url = 'https://chromedriver.storage.googleapis.com/' + chrome_version + '/chromedriver_win32.zip'
    elif sys.platform.startswith('darwin'):
        if platform.machine() == 'arm64':
            chromedriver_url = 'https://chromedriver.storage.googleapis.com/' + chrome_version + \
                               '/chromedriver_mac64_m1.zip'
        else:
            chromedriver_url = 'https://chromedriver.storage.googleapis.com/' + chrome_version + \
                               '/chromedriver_mac64.zip'
    else:
        logger.error('Error: 不支持的平台环境')
        raise TypeError('Error: 不支持的平台环境')
    logger.info('从"{}"下载Chrome驱动程序（版本：{}）'.format(chromedriver_url, chrome_version))
    with open(CHROMEDRIVER_ZIP_FILE, 'wb') as driver_zip:
        driver_zip.write(requests.get(chromedriver_url).content)
    with zipfile.ZipFile(CHROMEDRIVER_ZIP_FILE, 'r') as driver_zip:
        driver_zip.extractall(DATA_FOLDER)
    os.remove(CHROMEDRIVER_ZIP_FILE)
    chmod(path=CHROMEDRIVER_FILE, mode=777)
    mv(CHROMEDRIVER_FILE, path)


def get_firefox_driver(path):
    logger.warn('请访问：https://github.com/mozilla/geckodriver/releases/latest 下载符合您操作系统版本的驱动。')


def get_edge_driver(path):
    logger.warn('请访问：https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/ 下载符合您操作系统版本的驱动。')


def get_safari_driver(path):
    if not sys.platform.startswith('darwin'):
        logger.error('Error: 不支持的平台环境')
        raise TypeError('Error: 不支持的平台环境')
    logger.info("Safari浏览器包含了safaridriver。请打开Safari的‘偏好设置’-‘高级’，勾选'在菜单栏中显示‘开发’菜单'；"
                "‘开发’菜单，勾选‘允许远程自动化’。\n"
                "在终端中执行 safaridriver --enable 即可启用。")


def get_driver(browser_type: str, path):
    if path is not None and len(path.strip()) != 0:
        path = os.path.join(PROJECT_PATH, path) if not os.path.isabs(path) else path
    else:
        path = DEFAULT_DRIVER_PATH
    logger.info('请确认已经安装最新版的{}浏览器，驱动程序将保存在：{}'.format(browser_type, path))
    browser_type = browser_type.lower()
    if browser_type == 'chrome':
        get_chrome_driver(path)
    elif browser_type == 'firefox':
        get_firefox_driver(path)
    elif browser_type == 'edge':
        get_edge_driver(path)
    elif browser_type == 'safari':
        get_safari_driver(path)
    else:
        logger.error('不支持自动初始化的浏览器，请手动初始化')
        raise ValueError('不支持自动初始化的浏览器，请手动初始化')
