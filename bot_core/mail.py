# coding = utf-8
# author: holger version: 2.4
# license: AGPL-3.0
# belong: DailyReport-BotCore

import json

from EmailSender.sender import send_email
from bot_core.file import MAIL_FILE, SUCCESS_MAIL_FILE, FAIL_MAIL_FILE

with open(MAIL_FILE, 'r', encoding='utf-8') as _file:
    mail_config = json.load(_file)

_mail = mail_config['sender']
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


def success_mail(to, stu_id, detail):
    return _email(_success_template, to, stu_id, detail)


def fail_mail(to, stu_id, detail):
    return _email(_fail_template, to, stu_id, detail)


def _email(template, to, stu_id, detail):
    config = {
        'mail': _mail,
        'template': template,
        'receivers': []
    }
    config['template']['global']['replace'] = {
        'stu_id': stu_id,
        'detail': ', '.join(map(lambda x: ': '.join(map(str, x)), detail.items()))
    }
    statistic = 0
    for r in mail_config['receivers']:
        if len(r) == 0:
            continue
        config['receivers'].append({'email': r})
        statistic += 1
    for r in to:
        if len(r) == 0:
            continue
        config['receivers'].append({'email': r})
        statistic += 1
    if statistic <= 0:
        return True
    return send_email(config)
