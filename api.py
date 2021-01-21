# coding = utf-8
# author: holger version: 1.35
# license: AGPL-3.0

import os
import time
from datetime import datetime

import requests
import json
import webbrowser
import version
from copy import deepcopy

API = "https://api.holgerbest.top/DailyReport/"
VERSION_API = "https://api.holgerbest.top/DailyReport/version/"
MSG_BOX_API = "https://api.holgerbest.top/msgbox.html?msg="


def __msg_box(desc: str):
    """ 以弹出页面的形式提醒用户 """
    webbrowser.open(MSG_BOX_API + desc)


def __get_api(api: str) -> dict:
    """ GET API """
    r = requests.get(api)
    assert r.status_code == 200
    return json.loads(r.text)


def __get_config(api_root: str) -> dict:
    """ GET all APIs """
    api_lists = __get_api(api_root)['accessible']
    config = {}
    for api in api_lists:
        config[api['name']] = __get_api(api['path'])
        assert config[api['name']]['status'] == 'success'
    return config


def __merge(old_data: dict, new_data: dict) -> (dict, bool):
    """
    合并old_data，new_data两配置数据（dict类型）
    配置数据的键类型为str，值类型为str、dict、list、float中的一种。
    要求：old_data中所有的键值对都会保存，除非：
    对于new_data和old_data中共有的键：
    - 若值为dict类型，合并方法相同（即递归合并）；
    - 若值为float类型，不相等则覆盖old_data中对应数据；
    - 若值为str、list类型，则new_data中不为空且不相等的数据覆盖原数据。
    对于new_data中新增加的键，直接将键值对添加到合并结果。
    要求不改变old_data，new_data两配置数据，而是生成一个新的dict作为第一个返回值。
    如果发生了覆盖和新增，要求第二个返回值返回True，否则返回False。
    """
    # TODO: 此处算法效率较低，有待于进一步优化
    result = deepcopy(old_data)
    old_key = list(old_data.keys())
    new_key = list(new_data.keys())
    need_adjust = False
    for key in new_key:
        if key in old_key:
            if isinstance(old_data[key], dict):
                result[key], adjust = __merge(old_data[key], new_data[key])
                if adjust:
                    need_adjust = True
            elif isinstance(old_data[key], list) or isinstance(old_data[key], str):
                if len(new_data[key]) != 0 and result[key] != new_data[key]:
                    need_adjust = True
                    result[key] = deepcopy(new_data[key])
            else:
                if result[key] != new_data[key]:
                    need_adjust = True
                    result[key] = deepcopy(new_data[key])
        else:
            need_adjust = True
            result[key] = deepcopy(new_data[key])
    return result, need_adjust


def update_config():
    """ 更新配置文件 """
    config = __get_config(API)
    need_adjust = []
    for name, data in config.items():
        file_name = name + '.json'
        if os.path.isfile(file_name):
            with open(file_name, 'r', encoding='utf-8') as file:
                old_data = json.load(file)
            if version.check_version(old_data['_version'], data['_version']) > 0:
                __msg_box("版本号有误，请手动下载{}替换，详见： {}".format(file_name, API))
                raise RuntimeError("版本号有误")
            data, adjust = __merge(old_data, data)
            if adjust and name in ("user", "scheduler"):
                need_adjust.append(name)
        else:
            if name in ("user", "scheduler"):
                need_adjust.append(name)
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(json.dumps(data, indent=2, ensure_ascii=False))
    if len(need_adjust) != 0:
        __msg_box("DailyReport: {}配置需要更新<br />请打开相应的json文件，按照_notes提示更新配置文件<br />"
                  "若从main.py启动更新后需重启程序；若5分钟没有修改则程序可能会异常退出。".format(', '.join(need_adjust)))
        time.sleep(5 * 60)
        # raise RuntimeWarning("配置需要更新")
    else:
        print("config up to date")


def check_update_src():
    """ 检查软件是否有更新（通过检查版本号） """
    r = requests.get(VERSION_API)
    assert r.status_code == 200
    if version.check_version(version.VERSION, float(r.text)) < 0:
        __msg_box("DailyReport: 软件需要更新<br />请访问：https://github.com/HolgerZhang/DailyReport <br />更新后请重启程序。")
    else:
        print('src up tp date')


def update():
    check_update_src()
    update_config()


检查更新 = update


def check(need_check: bool, call_func):
    """ 检查更新装饰器 """

    def wrapper(func):
        def inner_wrapper():
            if need_check:
                print("{}时间:".format(call_func.__name__), datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                call_func()
            return func()

        return inner_wrapper

    return wrapper
