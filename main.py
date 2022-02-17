# coding = utf-8
# author: holger version: 2.5
# license: AGPL-3.0
# belong: DailyReport-Predefined

import argparse
import sys
import traceback

import api
import resources
from bot_core import bot, exec_log
from bot_core.exec_log import logger
from bot_core.file import get_driver, msg_box
from bot_core.mail import Mail
from bot_core.version import VERSION

parser = argparse.ArgumentParser(description="Daily health report automated program. 每日打卡自动化程序",
                                 formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-v", "--version", action="version",
                    version='Daily health report automated program. 每日打卡自动化程序\n'
                            'v{}  By @HolgerZhang, thanks @ygLance, @TTL2000.\n'
                            '    Together with SUMSC/email-sender v0.1.2\n'
                            'GitHub: https://github.com/HolgerZhang/DailyReport\n'
                    .format(VERSION))
group = parser.add_mutually_exclusive_group()
group.add_argument('-i', '--initialize', action='store_true',
                   help="initialize program")
group.add_argument('-u', '--update-only', action='store_true',
                   help="only update configuration")
parser.add_argument('-m', '--disable-monitor', action='store_true',
                    help="disable the 'automatic loading of file changes' feature")
parser.add_argument('-o', '--once', action='store_true',
                    help="run only once")
parser.add_argument('-l', '--local', action='store_true',
                    help="enable 'local run' feature, default disabled")
parser.add_argument('-idx', '--user-index', dest='index', type=int, default=-1,
                    help="run only the user configuration number 'index', default run all")
args = parser.parse_args()

# 文件变更自动加载特性
if args.disable_monitor:
    from bot_core.scheduler import Scheduler
else:
    from bot_core.monitor import Scheduler

# 核心类实例
_bot = bot.WebBot()
_scheduler = Scheduler()


def update():
    """ 检查更新 """
    if not args.local:
        api.update()
    _bot.load()
    if not args.once:
        _scheduler.load()


@api.check(not args.local, update)  # 自动检查更新特性
def job():
    """ 作业函数 """
    exec_log.logger('START')
    _bot.start()
    bot.run_bot(_bot, user_index=args.index)
    _bot.finish()
    exec_log.logger('FINISH')


def main():
    """ 主函数 """
    update()
    if args.once:
        job()
    else:
        _scheduler.schedule(job, _bot)


def init():
    print(resources.PROGRAM_SETUP)
    logger(resources.PROGRAM_SETUP)
    get_driver()
    api.update(timeout=0)
    msg_box(resources.START_INTRODUCTION, error=False)
    print(resources.START_INTRODUCTION)


if __name__ == '__main__':
    try:
        if args.initialize:
            init()
        elif args.update_only:
            api.update()
        else:
            main()
    except Exception as e:
        mail = Mail()
        mail.load()
        mail.fail_mail(to=[], stu_id='ALL',
                       detail={'<strong>未知错误</strong>': Mail.html('{} - {}'.format(e.__class__, e)),
                               'Stack': Mail.html(traceback.format_exc())})
        print(traceback.format_exc(), file=sys.stderr)
