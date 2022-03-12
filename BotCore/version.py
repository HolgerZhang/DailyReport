# coding = utf-8
# author: holger
# version: 4.0.0
# license: AGPL-3.0
# belong: DailyReport-BotCore

import json

from BotCore.file import VERSION_FILE

# 加载数据
with open(VERSION_FILE, 'r', encoding='utf-8') as __version_file:
    __version = json.load(__version_file)


def get_version_tuple(version_str: str):
    ver = []
    for item in version_str.strip().split('.')[:3]:
        if not item.isdigit():
            raise ValueError('版本号格式不符合要求！')
        ver.append(int(item))
    if not 2 <= len(ver) <= 3:
        raise ValueError('版本号格式不符合要求！')
    if len(ver) == 2:
        ver.append(0)
    return tuple(ver)


# 版本号
VERSION = get_version_tuple(__version['VERSION'])
MAPPING_MIN_VERSION = get_version_tuple(__version['MAPPING_MIN_VERSION'])
GENERAL_MIN_VERSION = get_version_tuple(__version['GENERAL_CONFIG_MIN_VERSION'])
USER_MIN_VERSION = get_version_tuple(__version['USER_CONFIG_MIN_VERSION'])


def check_version(version1: tuple, version2: tuple) -> bool:
    """
    比较两版本号差异
    :param version1: 3位版本号
    :param version2: 3位版本号
    :return: version1小于等于version2返回True
    """
    assert len(version1) == len(version2) == 3, '版本号格式不符合要求！'
    return version1 <= version2
