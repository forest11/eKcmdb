#!/usr/bin/env python3
# -*— coding: utf-8 -*-
# __author__ : pandonglin
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


def email(email_list, content, subject="eKing科技运维平台-找回密码"):
    """
    发送短信
    :param email_list:
    :param content:
    :param subject:
    :return:
    """
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = formataddr(["易建科技运维平台-系统邮件", 'pandonglin@makepolo.com'])
    msg['Subject'] = subject
    server = smtplib.SMTP("smtp.makepolo.com", 25)
    server.login("pandonglin@makepolo.com", "Python-147")
    server.sendmail('pandonglin@makepolo.com', email_list, msg.as_string())
    server.quit()
