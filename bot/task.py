# coding = utf-8
"""
file: bot/task.py
author: holger
version: 3.0
license: AGPL-3.0
belongs: WebBot-BotCore
"""
from apscheduler.schedulers.blocking import BlockingScheduler

from bot import core
from bot import exec_log
from bot import resources
from bot import util
from bot import xml_parser
from bot.resources import R


class TaskScheduler:
    """
    计划任务类（核心类）
    """

    def __init__(self):
        """
        构造函数
        """
        self._scheduler = util.SchedulerInfo()
        self._blocking_scheduler = BlockingScheduler()

    def load(self):
        """
        加载数据
        """
        self._scheduler = xml_parser.get_scheduler_cfg(resources.CONFIGURATION_FILE)
        exec_log.logger(resources.R.string.LOAD_SCHEDULER)

    def __watch(self, job, web_bot: core.WebBot):
        """
        监测文件变化
        :param job: 作业函数，无参数
        :param web_bot: WebBot 对象
        """
        if not util.same(self._scheduler):
            exec_log.logger(resources.R.string.FILE_CHANGED_F1.format(util.SchedulerInfo))
            self._blocking_scheduler.remove_all_jobs()
            self.load()
            self.add_job(job, web_bot)
            resources.copy_file(resources.CONFIGURATION_FILE)
        if not util.same(web_bot.mapping):
            exec_log.logger(resources.R.string.FILE_CHANGED_F1.format(util.Mapping))
            web_bot.load(map_name=web_bot.mapping_name)
            resources.copy_file(resources.MAP_FILE)
        if not util.same(web_bot.all_user):
            exec_log.logger(resources.R.string.FILE_CHANGED_F1.format(util.User))
            web_bot.load(map_name=web_bot.mapping_name)
            resources.copy_file(resources.CONFIGURATION_FILE)

    def add_job(self, job, web_bot: core.WebBot):
        """
        添加作业
        :param job: 作业函数，无参数
        :param web_bot: WebBot 对象
        """

        def watch():
            """
            包装 self.__watch 方法的无参函数
            """
            return self.__watch(job, web_bot)

        self._blocking_scheduler.add_job(job, 'cron', hour=self._scheduler.hour, minute=self._scheduler.minute,
                                         second=self._scheduler.second)
        self._blocking_scheduler.add_job(watch, 'cron', second=30)
        exec_log.logger(R.string.SCHEDULER_TAG +
                        ';\t'.join((str(x).replace('.<locals>', '') for x in self._blocking_scheduler.get_jobs())))

    def schedule(self, job, web_bot: core.WebBot):
        """
        创建调度器，配置和添加作业，并执行调度
        :param job: 作业函数，无参数
        :param web_bot: WebBot 对象
        """
        resources.copy_file()
        self.add_job(job, web_bot)
        self._blocking_scheduler.start()
