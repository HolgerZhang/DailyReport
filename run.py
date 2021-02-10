# coding = utf-8
# author: holger version: 2.0
# license: AGPL-3.0
# belong: DailyReport-Predefined

# use `--no-update` to disable file auto update feature
# use `--no-monitor` to disable file changes check feature
# use `--once` to run program once

import sys

import api
from bot_core import bot, exec_log

# 文件变更自动加载特性
if '--no-monitor' in sys.argv:
    from bot_core.scheduler import Scheduler
else:
    from bot_core.monitor import Scheduler

# 核心类实例
_bot = bot.WebBot()
_scheduler = Scheduler()


def update(once=False):
    """ 检查更新 """
    api.update()
    _bot.load()
    if not once:
        _scheduler.load()


# 自动检查更新特性
@api.check('--no-update' not in sys.argv, update)
def job():
    """ 作业函数 """
    exec_log.logger('START')
    _bot.start()
    bot.run_bot(_bot)
    _bot.finish()
    exec_log.logger('FINISH')


def run():
    """ 正常运行 """
    update()
    _scheduler.schedule(job, _bot)


def run_once():
    """ 运行一次 """
    update(once=True)
    job()


def main():
    """ 主函数 """
    if '--once' in sys.argv:
        run_once()
    else:
        run()


if __name__ == '__main__':
    main()
