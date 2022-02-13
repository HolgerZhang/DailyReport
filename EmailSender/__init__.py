# coding = utf-8
# author: SUMSC (holger) version: 0.1.2 (Beta), DailyReport version: 2.4
# license: LGPL-2.1
# belong: MailSender for DailyReport-Foreign-Project

import sys
import logging

if sys.platform.startswith('linux'):
    import encodings.idna

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)
__handler = logging.FileHandler('EmailSender.log', encoding='utf-8')
__handler.setLevel(logging.DEBUG)
__formatter = logging.Formatter('%(asctime)s %(threadName)s - %(module)s [%(levelname)s] %(message)s')
__handler.setFormatter(__formatter)
__console = logging.StreamHandler()
__console.setLevel(logging.INFO)
logger.addHandler(__handler)
logger.addHandler(__console)

