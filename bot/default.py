# coding = utf-8
"""
file: bot/default.py
author: holger
version: 3.0
license: AGPL-3.0
belongs: WebBot-Module
"""
from bot import exec_log
from bot.core import WebBot
from bot.resources import R
from bot.task import TaskScheduler

DefaultBot = WebBot()
DefaultScheduler = TaskScheduler()


def job_maker(**kwargs):
    map_name = kwargs.get('map_name', None)
    user_id = kwargs.get('user_id', None)
    before = kwargs.get('before', None)

    def run_function(func):
        def run_bot():
            exec_log.logger(R.string.START_JOB)
            if before is not None:
                before()
            DefaultBot.load(map_name)
            DefaultScheduler.load()
            DefaultBot.start()
            DefaultBot.go()
            DefaultBot.run(user_id)
            DefaultBot.finish()
            func()
            exec_log.logger(R.string.FINISH_JOB)

        return run_bot

    return run_function


@job_maker()
def default_job():
    pass


def default_run():
    run(default_job)


def run(job):
    DefaultScheduler.schedule(job=job, web_bot=DefaultBot)


def run_once(map_name=None, user_id=None):
    job_maker(map_name=map_name, user_id=user_id)(lambda: None)()
