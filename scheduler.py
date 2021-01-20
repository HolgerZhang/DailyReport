# coding = utf-8
# author: holger version: 1.3
# license: AGPL-3.0

# pip install apscheduler

import json
from apscheduler.schedulers.blocking import BlockingScheduler

import version

__scheduler = {}


def load():
    """ 加载数据 """
    global __scheduler
    with open('scheduler.json', 'r', encoding='utf-8') as __scheduler_file:
        __scheduler = json.load(__scheduler_file)
        assert version.check_version(version.SCHEDULER_MIN_VERSION_REQUIRED, __scheduler['_version']) <= 0
        __scheduler = __scheduler["scheduler"]


def schedule(job):
    """ 创建调度器（非阻塞），配置和添加作业，并执行调度 """
    scheduler = BlockingScheduler()
    scheduler.add_job(job, 'cron', year='*', month='*', day='*', week='*', day_of_week='*',
                      hour=__scheduler['hour'], minute=__scheduler['minute'])
    scheduler.start()


调度 = schedule
