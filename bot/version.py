# coding = utf-8
"""
file: bot/version.py
author: holger
version: 3.0
license: AGPL-3.0
belongs: WebBot-Module
"""

VERSION = 3.0
MAP_MIN_VERSION = 3.0
CONFIGURATION_MIN_VERSION = 3.0


def check_version(version1: float, version2: float) -> int:
    """
    比较两版本号差异
    :param version1: 版本号
    :param version2: 版本号
    :return: version1小于version2返回负数，相等返回0，大于返回正数
    """
    return int(100 * version1) - int(100 * version2)
