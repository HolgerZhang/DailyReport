# coding = utf-8
# author: holger version: 1.4
# license: AGPL-3.0

# use `--miss-feature` to disable file monitor feature

import os
import sys
import shutil
import json
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

import bot
import scheduler

FILE = ['scheduler.json', 'user.json', 'mapping.json']
TEMP_FOLDER = '.cmp_dat'
PATH_SPLIT = '\\' if sys.platform.lower() == 'win32' else '/'
_scheduler = BlockingScheduler()


def copy_file():
    if not os.path.isdir(TEMP_FOLDER):
        os.mkdir(TEMP_FOLDER)
    for file in FILE:
        shutil.copyfile(file, TEMP_FOLDER + PATH_SPLIT + file)


def same(old_data: dict, new_data: dict) -> bool:
    for key in old_data.keys():
        data = new_data.get(key)
        if isinstance(data, dict) and isinstance(old_data[key], dict) and not same(old_data[key], data):
            return False
        if old_data[key] != data:
            return False
    return True


def watch(job):
    """ 监测文件变化，每隔三分钟 """
    print('{}: 检查文件{}'.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ', '.join(FILE)))
    for file in FILE:
        with open(TEMP_FOLDER + PATH_SPLIT + file, 'r', encoding='utf-8') as old_file, \
                open(file, 'r', encoding='utf-8') as new_file:
            if same(json.load(old_file), json.load(new_file)):
                continue
        print('{}文件发生变化，正在应用更改.'.format(file))
        if file == 'scheduler.json':
            _scheduler.remove_all_jobs()
            scheduler.load()
            add_job(job)
        else:
            bot.load()
    copy_file()


def add_job(job):
    _scheduler.add_job(job, 'cron', year='*', month='*', day='*', week='*', day_of_week='*',
                       hour=scheduler.__scheduler['hour'], minute=scheduler.__scheduler['minute'])
    _scheduler.add_job(lambda: watch(job), 'cron', year='*', month='*', day='*', week='*', day_of_week='*',
                       hour='*', minute='*/3', second='30')


def schedule(job):
    copy_file()
    add_job(job)
    _scheduler.start()


调度 = schedule
