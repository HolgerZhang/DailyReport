# coding = utf-8
# author: SUMSC (holger)
# version: 0.1.2 (Beta), DailyReport version: 4.0.0
# license: LGPL-2.1
# belong: MailSender for DailyReport-Foreign-Project

import os
import smtplib
import traceback
import threadpool

from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

from easydict import EasyDict

from EmailSender import logger
from EmailSender.generator import Email, EmailTemplate


class Sender:
    def __init__(self, smtp_host: str, mail_user: str, mail_passwd: str, ssl_port: int,
                 sender_name=None, starttls=False):
        self._smtp_host: str = smtp_host  # 设置服务器
        self._mail_user: str = mail_user  # 用户名
        self._mail_passwd: str = mail_passwd  # 口令
        self._ssl_port: int = ssl_port
        self.__sender_header = formataddr((sender_name if sender_name is not None else mail_user, mail_user), 'utf-8')
        self._starttls = starttls

    def send(self, email: Email):
        if email.attachments is None:
            message = MIMEText(email.content, 'html', 'utf-8')
        else:
            message = MIMEMultipart()
            message.attach(MIMEText(email.content, 'html', 'utf-8'))
        message['From'] = self.__sender_header
        message['To'] = formataddr((email.receiver_name, email.receiver), 'utf-8')
        message['Subject'] = Header(email.subject, 'utf-8')
        if email.attachments is not None:
            for attachment in email.attachments:
                att = MIMEText(open(attachment, 'rb').read(), 'base64', 'utf-8')
                att["Content-Type"] = 'application/octet-stream'
                att["Content-Disposition"] = f'attachment; filename="{os.path.basename(attachment)}"'
                message.attach(att)
                logger.info(f'attachment "{os.path.basename(attachment)}" added. (email_id={hex(id(email))})')
        ret = True
        try:
            logger.info(f'Sending email from `{self._mail_user}` to `{email.receiver}`... (email_id={hex(id(email))})')
            if self._starttls:
                server = smtplib.SMTP(self._smtp_host, self._ssl_port)
                server.starttls()
            else:
                server = smtplib.SMTP_SSL(self._smtp_host, self._ssl_port)
            server.login(self._mail_user, self._mail_passwd)
            server.sendmail(self._mail_user, [email.receiver], message.as_string())
            server.close()
            logger.info(f'Email<`{self._mail_user}` -> `{email.receiver}`> sent successfully! '
                        f'(email_id={hex(id(email))})')
        except (smtplib.SMTPException, TimeoutError) as e:
            logger.error(f'Sent email<`{self._mail_user}` -> `{email.receiver}`> failed! (email_id={hex(id(email))})'
                         f'Encountered an error named {e.__class__.__name__}: {e}.')
            logger.debug(f'Exception Stack information: \n{traceback.format_exc()}')
            ret = False
        return ret


def send_email(config, thread_pool_size=32):
    if not isinstance(config, EasyDict):
        config = EasyDict(config)
    assert config.get('mail') is not None, 'config file is incomplete!'
    # config.mail
    try:
        sender = Sender(smtp_host=config.mail.host,
                        mail_user=config.mail.user,
                        mail_passwd=config.mail.passwd,
                        ssl_port=config.mail.port,
                        starttls=config.mail.get('starttls', False),
                        sender_name=config.mail.get('name', None))
    except AttributeError:
        logger.error('config.mail configuration is incomplete!')
        return False
    assert config.get('template') is not None, 'config file is incomplete!'
    # config.template
    if config.template.get('use_file', False):
        try:
            template = EmailTemplate(config.template.file, use_file=True)
        except AttributeError:
            logger.error('config.template.file is required when config.template.use_file is true!')
            return False
    else:
        try:
            template = EmailTemplate(config.template.content)
        except AttributeError:
            logger.error('config.template.content is required when config.template.use_file is false or not given!')
            return False
    global_config = config.template.get('global', EasyDict())
    assert config.get('receivers') is not None, 'config file is incomplete!'
    # config.receivers
    count = len(config.receivers)
    failed = []
    email_list = []
    for receiver in config.receivers:
        email = receiver.email
        name = receiver.get('name', None)
        subject = receiver.get('subject', global_config.subject)
        attachments = receiver.get('attachments', global_config.get('attachments', None))
        replace = global_config.get('replace', EasyDict())
        replace.update(receiver.get('replace', dict()))
        email_obj = template.generator(email, subject, name, attachments, **replace)
        email_list.append(email_obj)

    def callback(req, ret):
        if not ret:
            failed.append((email, name))

    pool = threadpool.ThreadPool(max(thread_pool_size, count))
    for request in threadpool.makeRequests(sender.send, email_list, callback=callback):
        pool.putRequest(request)
    pool.wait()
    if len(failed) == count:
        logger.error('All emails failed to be sent!')
        return False
    if 0 < len(failed) < count:
        logger.warning(f'Some emails failed to be sent! '
                       f'they are: {failed}')
        return True
    logger.info('All emails were sent successfully!')
    return True
