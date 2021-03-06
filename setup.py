# coding = utf-8
# author: holger version: 2.0
# license: AGPL-3.0
# belong: DailyReport-Predefined

import os

import resources
from api import update
from bot_core.exec_log import logger
from bot_core.file import msg_box, get_driver

print(resources.PROGRAM_SETUP)
logger(resources.PROGRAM_SETUP)
get_driver()
os.system('pip install -r requirement.txt')
update(timeout=0)
msg_box(resources.START_INTRODUCTION)
print(resources.START_INTRODUCTION)
