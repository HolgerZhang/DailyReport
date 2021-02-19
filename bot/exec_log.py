# coding = utf-8
"""
file: bot/exec_log.py
author: holger
version: 3.0
license: AGPL-3.0
belongs: WebBot-BotCore
"""

from datetime import datetime

from bot import resources


def logger(arg: str):
    """
    写入日志
    :param arg: 写入字符串
    :return: None
    """
    with open(resources.LOG_FILE, 'a', encoding='utf-8') as log_file:
        log_file.write('[{}] '.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + arg + '\n')
        log_file.flush()


def text_saver(arg: str):
    """
    写入文件
    :param arg: 写入字符串
    :return: None
    """
    with open(resources.TEXT_SAVE_FILE, 'a', encoding='utf-8') as log_file:
        log_file.write('[{}] '.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + arg + '\n')
        log_file.flush()
