# coding = utf-8
# author: holger version: 2.0
# license: AGPL-3.0
# belong: DailyReport-BotCore

import json

from apscheduler.schedulers.blocking import BlockingScheduler

from bot_core import bot, version, exec_log, resources
from bot_core.file import SCHEDULER_FILE


class Scheduler:
    """
    计划任务类（核心类）
    """
    def __init__(self):
        """
        构造函数
        """
        self.__scheduler = {}

    def load(self):
        """
        加载数据
        """
        with open(SCHEDULER_FILE, 'r', encoding='utf-8') as __scheduler_file:
            self.__scheduler = json.load(__scheduler_file)
            assert version.check_version(version.SCHEDULER_MIN_VERSION_REQUIRED, self.__scheduler['_version']) <= 0
            self.__scheduler = self.__scheduler["scheduler"]
        if len(self.__scheduler['hour']) == 0:
            self.__scheduler['hour'] = '9'
        if len(self.__scheduler['minute']) == 0:
            self.__scheduler['minute'] = '30'
        exec_log.logger(resources.LOAD_SCHEDULER_JSON)

    def schedule(self, job, web_bot: bot.WebBot):
        """
        创建调度器，配置和添加作业，并执行调度
        :param job: 作业函数，无参数
        :param web_bot: WebBot 对象（预留接口）
        """
        scheduler = BlockingScheduler()
        scheduler.add_job(job, 'cron', year='*', month='*', day='*', week='*', day_of_week='*',
                          hour=self.__scheduler['hour'], minute=self.__scheduler['minute'])
        scheduler.start()
