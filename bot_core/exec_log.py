# coding = utf-8
# author: holger version: 2.5
# license: AGPL-3.0
# belong: DailyReport-BotCore

import logging

_logger = logging.getLogger(__name__)
_logger.setLevel(level=logging.DEBUG)
handler = logging.FileHandler('BotLog.log')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(threadName)s - [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
_logger.addHandler(handler)
_logger.addHandler(console)


def logger(arg: str, level='info') -> None:
    """
    写入日志
    :param arg: 写入字符串
    :param level: 等级
    :return: None
    """
    if level.lower() == 'info':
        _logger.info(arg)
    elif level.lower() == 'debug':
        _logger.debug(arg)
    elif level.lower() == 'warn':
        _logger.warning(arg)
    elif level.lower() == 'error':
        _logger.error(arg)
