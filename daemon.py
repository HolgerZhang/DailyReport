# coding = utf-8
# author: holger
# version: 4.0.0
# license: AGPL-3.0
# belong: DailyReport-DaemonProcess
import json
import os.path
import sys

import threadpool
from apscheduler.schedulers.blocking import BlockingScheduler
from easydict import EasyDict
from pyvirtualdisplay import Display

import api
from BotCore import logger
from BotCore.bot import WebBot, run_bot
from BotCore.file import MAPPING_FILE, PROJECT_PATH, DEFAULT_DRIVER_PATH
from mail import Mail


def wakeup(user_config_path: str, users: list, bot_config: EasyDict, mail: Mail, thread_pool_size=16, update_=True):
    def task(bot: WebBot):
        logger.info('START, ' + bot.user['user_id'])
        bot.start()
        run_bot(bot, mail)
        bot.finish()
        logger.info('FINISH, ' + bot.user['user_id'])

    if update_:
        update()
    bot_list = []
    for user_name in users:
        user_file = os.path.join(user_config_path, 'user.{}.json'.format(user_name))
        if not os.path.isabs(user_file):
            user_file = os.path.join(PROJECT_PATH, user_file)
        if not os.path.exists(user_file):
            logger.error('文件{}不存在，跳过该文件'.format(user_file))
            continue
        if bot_config.driver_path is not None and len(bot_config.driver_path.strip()) != 0:
            driver_path = os.path.join(PROJECT_PATH, bot_config.driver_path) \
                if not os.path.isabs(bot_config.driver_path) else bot_config.driver_path
        else:
            driver_path = DEFAULT_DRIVER_PATH
        bot_list.append(WebBot(user_file, bot_config.browser, driver_path))
    logger.info('使用多个线程执行')
    pool = threadpool.ThreadPool(thread_pool_size)
    for req in threadpool.makeRequests(task, bot_list):
        pool.putRequest(req)
    pool.wait()
    logger.info('线程执行完成')


def update():
    api.check_update_src()
    mapping = api.get_new_api(api.MAPPING_API_V4)
    logger.info('从"{}"更新文件"{}"'.format(api.MAPPING_API_V4, MAPPING_FILE))
    with open(MAPPING_FILE, 'w', encoding='utf-8') as _file:
        _file.write(json.dumps(mapping, indent=2, ensure_ascii=False))


def new_user(user_config_path: str , name: str):
    file_path = os.path.join(user_config_path, 'user.{}.json'.format(name))
    if not os.path.isabs(file_path):
        file_path = os.path.join(PROJECT_PATH, file_path)
    if os.path.exists(file_path):
        logger.error('文件"{}"已经存在！'.format(file_path))
        return
    user = api.get_new_api(api.USER_API_V4)
    logger.info('从"{}"下载文件"{}"'.format(api.USER_API_V4, file_path))
    with open(file_path, 'w', encoding='utf-8') as _file:
        _file.write(json.dumps(user, indent=2, ensure_ascii=False))


def schedule(hour, minute, enable=True):
    def function(func):
        def with_args(*args, **kwargs):
            if enable:
                def task():
                    func(*args, **kwargs)

                scheduler = BlockingScheduler()
                scheduler.add_job(task, 'cron', year='*', month='*', day='*', week='*', day_of_week='*',
                                  hour=str(hour), minute=str(minute))
                logger.info('计划任务: ' + '; '.join((str(x).replace('.<locals>', '') for x in scheduler.get_jobs())))
                scheduler.start()
            else:
                func(*args, **kwargs)

        return with_args

    return function


def virtual_display(turn_on):
    def function(func):
        def with_args(*args, **kwargs):
            if turn_on:
                if sys.platform.startswith('linux'):
                    logger.info('使用虚拟桌面Xvfb运行')
                    display = Display(visible=False, size=(900, 800))
                    display.start()
                    func(*args, **kwargs)
                    display.stop()
                else:
                    logger.warn('Xvfb仅支持Linux平台，将以默认模式运行')
                    func(*args, **kwargs)
            else:
                func(*args, **kwargs)

        return with_args

    return function
