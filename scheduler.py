# coding = utf-8
# author: holger version: 1.21
# license: AGPL-3.0

# pip install apscheduler

import json
from apscheduler.schedulers.blocking import BlockingScheduler

from version import VERSION, SCHEDULER_MIN_VERSION_REQUIRED

# Load
with open('scheduler.json', 'r', encoding='utf-8') as __scheduler_file:
    __scheduler = json.load(__scheduler_file)
    assert SCHEDULER_MIN_VERSION_REQUIRED <= __scheduler['_version'] <= VERSION
    __scheduler = __scheduler["scheduler"]


def schedule(job):
    """ 创建调度器（非阻塞），配置和添加作业，并执行调度 """
    scheduler = BlockingScheduler()
    scheduler.add_job(job, 'cron', year='*', month='*', day='*', week='*', day_of_week='*',
                      hour=__scheduler['hour'], minute=__scheduler['minute'])
    scheduler.start()


调度 = schedule
