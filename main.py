# coding = utf-8
# author: holger version: 1.2
# license: AGPL-3.0

import bot
import scheduler

from datetime import datetime


def 作业():
    print("打卡时间:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    打卡机器人 = bot.DailyReport()
    if 打卡机器人.需要登录():
        打卡机器人.登录()
    打卡机器人.打卡()


if __name__ == '__main__':
    scheduler.调度(作业)
