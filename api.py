# coding = utf-8
# author: holger version: 4.0.1
# license: AGPL-3.0
# belong: DailyReport-API

import json

import requests

from BotCore import version, logger

# APIs
MAPPING_API_V4 = "https://api.holgerbest.top/DailyReport/v4/mapping/"
USER_API_V4 = "https://api.holgerbest.top/DailyReport/v4/user/"
VERSION_API_V4 = "https://api.holgerbest.top/DailyReport/v4/version/"


def get_new_api(api: str) -> dict:
    """ GET API_V2 """
    r = requests.get(api)
    assert r.status_code == 200
    return json.loads(r.text)


def check_update_src():
    """ 检查软件是否有更新（通过检查版本号） """
    r = requests.get(VERSION_API_V4)
    assert r.status_code == 200
    if not version.check_version(version.VERSION, version.get_version_tuple(r.text)):
        logger.warn("软件需要更新! 请访问：https://github.com/HolgerZhang/DailyReport/releases/tag/v{}\n"
                    "更新后请重启程序。".format(r.text))
    else:
        logger.debug("程序版本已是最新")
