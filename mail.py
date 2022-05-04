# coding = utf-8
# author: holger
# version: 4.0.0
# license: AGPL-3.0
# belong: DailyReport-Mail
from copy import deepcopy

from BotCore import logger
from BotCore.file import SUCCESS_MAIL_FILE, FAIL_MAIL_FILE
from EmailSender.sender import send_email


class Mail:

    @staticmethod
    def html(s):
        return s.replace('"', '&#x22;') \
            .replace('<', '&#x3c;') \
            .replace('>', '&#x3e;') \
            .replace("'", '&#x27;') \
            .replace('\n', '<br />')

    def __init__(self, config):
        self.__mail_config = config
        self.__mail = self.__mail_config['sender']
        assert len(self.__mail['user']) != 0 and len(self.__mail['passwd']) != 0 and len(self.__mail['host']) != 0

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
        to = list(to)
        to.extend(self.__mail_config['receivers'])
        return self.__email(self._fail_template, to, stu_id, detail)

    def __email(self, template, to, stu_id, detail):
        detail = deepcopy(detail)
        if detail.get('__notes') is not None:
            del detail['__notes']
        if detail.get('password') is not None:
            detail['password'] = '*' * 8
        config = {
            'mail': self.__mail,
            'template': template,
            'receivers': []
        }
        config['template']['global']['replace'] = {
            'stu_id': stu_id,
            'detail': '<ul>' + '\n'.join(map(lambda x: '<li>' + Mail.html(': '.join(map(str, x))) + '</li>',
                                             detail.items())) + '</ul>'
        }
        receivers = set(filter(lambda x: len(x) > 0, to))
        if len(receivers) == 0:
            return True
        for receiver in receivers:
            config['receivers'].append({'email': receiver})
        ret = send_email(config, wait=True)
        if not ret:
            logger.warning('邮件未能成功发送，详情请查看EmailSender.log！')
        return ret
