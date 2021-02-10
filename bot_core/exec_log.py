# coding = utf-8
# author: holger version: 2.0
# license: AGPL-3.0
# belong: DailyReport-BotCore

from datetime import datetime

from bot_core import file


def logger(arg: str) -> None:
    """
    写入日志
    :param arg: 写入字符串
    :return: None
    """
    with open(file.LOG_FILE, 'a', encoding='utf-8') as log_file:
        log_file.write('[{}] '.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + arg + '\n')
        log_file.flush()
