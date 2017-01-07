#!/usr/bin/env python3
# -*— coding: utf-8 -*-
# __author__ : pandonglin
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


def email(email_list, content, subject="马可波罗运维平台-找回密码"):
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = formataddr(["马可波罗运维平台-系统邮件", 'pandonglin@makepolo.com'])
    msg['Subject'] = subject
    server = smtplib.SMTP("smtp.makepolo.com", 25)
    server.login("pandonglin@makepolo.com", "password")
    server.sendmail('pandonglin@makepolo.com', email_list, msg.as_string())
    server.quit()
