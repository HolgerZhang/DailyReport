# coding = utf-8
# author: holger version: 2.5
# license: AGPL-3.0
# belong: DailyReport-BotCore

import json

from EmailSender.sender import send_email
from bot_core import version, exec_log, resources
from bot_core.file import MAIL_FILE, SUCCESS_MAIL_FILE, FAIL_MAIL_FILE


class Mail:

    @staticmethod
    def html(s):
        return s.replace('"', '&#x22;') \
            .replace('<', '&#x3c;') \
            .replace('>', '&#x3e;') \
            .replace("'", '&#x27;') \
            .replace('\n', '<br />')

    def __init__(self):
        self.__mail = {}
        self.__mail_config = {}

    def load(self) -> None:
        """
        加载数据
        :return: None
        """
        with open(MAIL_FILE, 'r', encoding='utf-8') as __file:
            self.__mail_config = json.load(__file)
            assert version.check_version(version.MAIL_MIN_VERSION_REQUIRED, self.__mail_config['_version']) <= 0
            self.__mail = self.__mail_config['sender']
            assert len(self.__mail['user']) != 0 and len(self.__mail['passwd']) != 0 and len(self.__mail['host']) != 0
        exec_log.logger(resources.LOAD_MAIL_JSON)

    _success_template = {
        'use_file': True,
        'file': SUCCESS_MAIL_FILE,
        'global': {
            'subject': '每日健康打卡 - 执行成功'
        }
    }
    _fail_template = {
        'use_file': True,
        'file': FAIL_MAIL_FILE,
        'global': {
            'subject': '每日健康打卡 - 执行失败'
        }
    }

    def success_mail(self, to, stu_id, detail):
        return self.__email(self._success_template, to, stu_id, detail)

    def fail_mail(self, to, stu_id, detail):
        return self.__email(self._fail_template, to, stu_id, detail)

    def __email(self, template, to, stu_id, detail):
        config = {
            'mail': self.__mail,
            'template': template,
            'receivers': []
        }
        config['template']['global']['replace'] = {
            'stu_id': stu_id,
            'detail': ', '.join(map(lambda x: ': '.join(map(str, x)), detail.items())).replace('\n', '<br />')
        }
        receivers = list(to)
        receivers.extend(self.__mail_config['receivers'])
        receivers = set(filter(lambda x: len(x) > 0, receivers))
        if len(receivers) == 0:
            return True
        for receiver in receivers:
            config['receivers'].append({'email': receiver})
        return send_email(config)
