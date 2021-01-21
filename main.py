# coding = utf-8
# author: holger version: 1.35
# license: AGPL-3.0

# use `--miss-feature` to disable file auto update feature

import sys
import bot
import scheduler
import api

from datetime import datetime


def 更新():
    api.检查更新()
    bot.load()
    scheduler.load()


@api.check('--miss-feature' not in sys.argv, 更新)
def 作业():
    print("打卡时间:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    打卡机器人 = bot.DailyReport()
    if 打卡机器人.需要登录():
        打卡机器人.登录()
    打卡机器人.打卡()


if __name__ == '__main__':
    更新()
    scheduler.调度(作业)
