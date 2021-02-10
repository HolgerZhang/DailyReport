# coding = utf-8
# author: holger version: 2.0
# license: AGPL-3.0
# belong: DailyReport-BotCore

import json

from apscheduler.schedulers.blocking import BlockingScheduler

from bot_core import bot, exec_log, scheduler
from bot_core import resources
from bot_core.file import FILE, same, copy_file, get_cmp_file


class Scheduler(scheduler.Scheduler):
    """
    计划任务类（核心类）（重写）
    """

    def __init__(self):
        """
        构造函数
        """
        self._blocking_scheduler = BlockingScheduler()
        super().__init__()

    def __watch(self, job, web_bot: bot.WebBot):
        """
        监测文件变化
        :param job: 作业函数，无参数
        :param web_bot: WebBot 对象
        """
        for file in FILE:
            with open(get_cmp_file(file), 'r', encoding='utf-8') as old_file, \
                    open(file, 'r', encoding='utf-8') as new_file:
                if same(json.load(old_file), json.load(new_file)):
                    continue
            exec_log.logger(resources.FILE_CHANGED_F1.format(file))
            copy_file(file)
            if file.endswith('scheduler.json'):
                self._blocking_scheduler.remove_all_jobs()
                self.load()
                self.add_job(job, web_bot)
            else:
                web_bot.load()

    def add_job(self, job, web_bot: bot.WebBot):
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

        self._blocking_scheduler.add_job(job, 'cron', year='*', month='*', day='*', week='*', day_of_week='*',
                                         hour=self.__scheduler['hour'], minute=self.__scheduler['minute'])
        self._blocking_scheduler.add_job(watch, 'cron', year='*', month='*', day='*', week='*', day_of_week='*',
                                         hour='*', minute='*', second='30')
        exec_log.logger(
            '计划任务:\n\t' + ';\n\t'.join((str(x).replace('.<locals>', '') for x in self._blocking_scheduler.get_jobs())))

    def schedule(self, job, web_bot: bot.WebBot):
        """
        创建调度器，配置和添加作业，并执行调度
        :param job: 作业函数，无参数
        :param web_bot: WebBot 对象
        """
        copy_file()
        self.add_job(job, web_bot)
        self._blocking_scheduler.start()
