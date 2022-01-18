# coding = utf-8
# author: holger version: 2.0
# license: AGPL-3.0
# belong: DailyReport-Predefined

import json
import os
import time
from copy import deepcopy

import requests

import resources
from bot_core import version
from bot_core.file import msg_box, get_file
from bot_core.exec_log import logger

# APIs


def __get_api(api: str) -> dict:
    """ GET API_V2 """
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


def __merge(old_data: dict, new_data: dict):
    """
    合并old_data，new_data两配置数据（dict类型）
    配置数据的键类型为str，值类型为str、dict、list、float中的一种。
    要求：old_data中所有的键值对都会保存，除非：
    对于new_data和old_data中共有的键：
    - 若值为dict类型，合并方法相同（即递归合并）；
    - 若值为float类型，不相等则覆盖old_data中对应数据；
    - 若值为str类型，则new_data中不为空且不相等的数据覆盖原数据；
    - 若值为list类型，则保持不变。
    对于new_data中新增加的键，直接将键值对添加到合并结果。
    要求不改变old_data，new_data两配置数据，而是生成一个新的dict作为第一个返回值。
    如果发生了覆盖和新增，要求第二个返回值返回True，否则返回False。
    """
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
            elif isinstance(old_data[key], str):
                if len(new_data[key]) != 0 and result[key] != new_data[key]:
                    need_adjust = True
                    result[key] = deepcopy(new_data[key])
            elif isinstance(old_data[key], list):
                result[key] = deepcopy(old_data[key])
            else:
                if result[key] != new_data[key]:
                    need_adjust = True
                    result[key] = deepcopy(new_data[key])
        else:
            need_adjust = True
            result[key] = deepcopy(new_data[key])
    return result, need_adjust


def update_config(timeout: float):
    """ 更新配置文件 """
    config = __get_config(resources.API_V2)
    need_adjust = []
    for name, data in config.items():
        file_name = get_file(name)
        if os.path.isfile(file_name):
            with open(file_name, 'r', encoding='utf-8') as file:
                old_data = json.load(file)
            if version.check_version(old_data['_version'], data['_version']) > 0:
                msg_box(resources.ERR_WRONG_VER_F2.format(file_name, resources.API_V2))
                raise RuntimeError(resources.ERR_WRONG_VER_F2.format(file_name, resources.API_V2))
            data, adjust = __merge(old_data, data)
            if adjust and name in ("user", "scheduler"):
                need_adjust.append(name)
        else:
            if name in ("user", "scheduler"):
                need_adjust.append(name)
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(json.dumps(data, indent=2, ensure_ascii=False))
    if len(need_adjust) != 0:
        msg_box(resources.CONFIG_NEED_UPDATE_F2.format(', '.join(need_adjust), timeout))
        time.sleep(timeout)
    else:
        logger(resources.CONFIG_UP_TO_DATE, level='debug')


def check_update_src():
    """ 检查软件是否有更新（通过检查版本号） """
    r = requests.get(resources.VERSION_API_V2)
    assert r.status_code == 200
    if version.check_version(version.VERSION, float(r.text)) < 0:
        msg_box(resources.SRC_NEED_UPDATE)
    else:
        logger(resources.SRC_UP_TO_DATE, level='debug')


def update(timeout=None):
    """
    检查更新
    :param timeout: 等待时间
    """
    check_update_src()
    update_config(timeout=timeout if timeout is not None else 5 * 60)


def check(need_check: bool, call_func):
    """ 检查更新装饰器 """

    def check_update(func):
        def check_update_inner():
            if need_check:
                logger(resources.RUN_F1.format(call_func.__name__), 'debug')
                call_func()
            return func()

        return check_update_inner

    return check_update
