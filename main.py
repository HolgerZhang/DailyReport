# coding = utf-8
# author: holger version: 1.1
# license: AGPL-3.0

import bot

打卡机器人 = bot.DailyReport()
if 打卡机器人.需要登录():
    打卡机器人.登录()
打卡机器人.打卡()
