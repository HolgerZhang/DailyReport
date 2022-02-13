# coding = utf-8
# author: holger version: 2.4
# license: AGPL-3.0
# belong: DailyReport-Predefined

import json
import os

import requests
import resources
from api import update
from bot_core.exec_log import logger
from bot_core.file import msg_box, get_driver, MAIL_FILE

if not os.path.exists(MAIL_FILE):
    r = requests.get(resources.API_V2_MAIL_API)
    assert r.status_code == 200
    with open(MAIL_FILE, 'w', encoding='utf-8') as _f:
        _f.write(json.dumps(json.loads(r.text), indent=2))

print(resources.PROGRAM_SETUP)
logger(resources.PROGRAM_SETUP)
get_driver()
os.system('python -m pip install -r requirements.txt')
update(timeout=0)
msg_box(resources.START_INTRODUCTION, error=False)
print(resources.START_INTRODUCTION)
