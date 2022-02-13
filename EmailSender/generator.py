# coding = utf-8
# author: SUMSC (holger) version: 0.1.2 (Beta), DailyReport version: 2.4
# license: LGPL-2.1
# belong: MailSender for DailyReport-Foreign-Project

from EmailSender import logger
import re


class Email:
    def __init__(self, receiver: str, subject: str, receiver_name=None):
        self._receiver = receiver
        self._receiver_name = receiver_name if receiver_name is not None else receiver
        self._subject = subject
        self._attachments = None
        self._content = ''

    @property
    def receiver(self):
        return self._receiver

    @property
    def receiver_name(self):
        return self._receiver_name

    @receiver_name.setter
    def receiver_name(self, name):
        self._receiver_name = name if name is not None else self.receiver

    @property
    def subject(self):
        return self._subject

    @subject.setter
    def subject(self, sub):
        self._subject = sub

    @property
    def attachments(self):
        return self._attachments

    def add_attachment(self, file_path):
        if self._attachments is None:
            self._attachments = [file_path]
        else:
            self._attachments.append(file_path)

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, c):
        self._content = c


class EmailTemplate:
    def __init__(self, template, use_file=False):
        if not use_file:
            self.template = template
        else:
            with open(template, 'r', encoding='utf-8') as file:
                self.template = file.read()

    def match(self, email_id, **kwargs):
        pattern = re.compile(rf'{{\s*%\s*(({")|(".join(kwargs.keys())}))\s*%\s*}}')

        def repl(match):
            target = kwargs[match.group(1)]
            logger.info(f'replacement: "{match.group(0)}" -> "{target}" (email_id={hex(email_id)})')
            return target

        result, count = pattern.subn(repl, self.template)
        logger.info(f'{count} substitutions have been completed. (email_id={hex(email_id)})')
        return result

    def generator(self, receiver: str, subject: str, receiver_name=None, attachments=None, **kwargs):
        email = Email(receiver, subject, receiver_name)
        if attachments:
            for attachment in attachments:
                email.add_attachment(attachment)
        email.content = self.match(email_id=id(email), **kwargs)
        return email
