# coding = utf-8
# author: holger
# version: 4.0.0
# license: AGPL-3.0
# belong: DailyReport-BotCore

import logging

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)
__handler = logging.FileHandler('BotLog.log')
__handler.setLevel(logging.DEBUG)
__formatter = logging.Formatter('%(asctime)s |%(process)d| %(threadName)s - %(module)s [%(levelname)s] %(message)s')
__handler.setFormatter(__formatter)
__console = logging.StreamHandler()
__console.setLevel(logging.INFO)
logger.addHandler(__handler)
logger.addHandler(__console)
