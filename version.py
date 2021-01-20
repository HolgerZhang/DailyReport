# coding = utf-8
# author: holger version: 1.3
# license: AGPL-3.0

import json

# Load
with open('version.json', 'r', encoding='utf-8') as __version_file:
    __version = json.load(__version_file)

VERSION = __version['VERSION']
MAPPING_MIN_VERSION_REQUIRED = __version['MAPPING_MIN_VERSION_REQUIRED']
USER_MIN_VERSION_REQUIRED = __version['USER_MIN_VERSION_REQUIRED']
SCHEDULER_MIN_VERSION_REQUIRED = __version['SCHEDULER_MIN_VERSION_REQUIRED']


def check_version(version1: float, version2: float) -> int:
    """ 比较两版本号差异，version1小于version2返回负数，相等返回0，大于返回正数 """
    return int(100 * version1) - int(100 * version2)
