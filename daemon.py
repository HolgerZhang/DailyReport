# coding = utf-8
# author: holger
# version: 4.0.0
# license: AGPL-3.0
# belong: DailyReport-DaemonProcess
import json
import os.path

import threadpool
from apscheduler.schedulers.blocking import BlockingScheduler
from easydict import EasyDict
from pyvirtualdisplay import Display

import api
from BotCore import logger
from BotCore.bot import WebBot, run_bot
from BotCore.file import MAPPING_FILE, PROJECT_PATH
from mail import Mail


def wakeup(user_config_path: str, users: list, bot_config: EasyDict, mail: Mail, thread_pool_size=16, update_=True):
    def task(bot: WebBot):
        logger.info('START')
        bot.start()
        run_bot(bot, mail)
        bot.finish()
        logger.info('FINISH')

    if update_:
        update()
    bot_list = []
    for user_name in users:
        user_file = os.path.join(user_config_path, 'user.{}.json'.format(user_name))
        if not os.path.isabs(user_file):
            user_file = os.path.join(PROJECT_PATH, user_file)
        driver_path = os.path.join(PROJECT_PATH, bot_config.driver_path) \
            if not os.path.isabs(bot_config.driver_path) else bot_config.driver_path
        bot_list.append(WebBot(user_file, bot_config.browser, driver_path))
    pool = threadpool.ThreadPool(thread_pool_size)
    for req in threadpool.makeRequests(task, bot_list):
        pool.putRequest(req)
    pool.wait()


def update():
    api.check_update_src()
    mapping = api.get_new_api(api.MAPPING_API_V4)
    with open(MAPPING_FILE, 'w', encoding='utf-8') as _file:
        _file.write(json.dumps(mapping, indent=2, ensure_ascii=False))


def schedule(hour, minute, enable=True):
    def function(func):
        def with_args(*args, **kwargs):
            if enable:
                def task():
                    func(*args, **kwargs)

                scheduler = BlockingScheduler()
                scheduler.add_job(task, 'cron', year='*', month='*', day='*', week='*', day_of_week='*',
                                  hour=str(hour), minute=str(minute))
                scheduler.start()
            else:
                func(*args, **kwargs)

        return with_args

    return function


def virtual_display(turn_on):
    def function(func):
        def with_args(*args, **kwargs):
            if turn_on:
                display = Display(visible=False, size=(900, 800))
                display.start()
                func(*args, **kwargs)
                display.stop()
            else:
                func(*args, **kwargs)

        return with_args

    return function
