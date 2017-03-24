#!/usr/bin/env python3
# -*— coding: utf-8 -*-
# __author__ : pandonglin
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings


def send_mail(to_mail, content, subject):
    """
    发送邮件
    :param to_mail_list:
    :param subject:
    :param content:
    :return:
    """
    me = "<" + settings.EMAIL_USER + ">"
    body = MIMEText(content)
    msg = MIMEMultipart()
    msg['Subject'] = "eking运维平台-%s" % subject
    msg['From'] = me
    msg['To'] = ";".join(to_mail)
    msg.attach(body)
    try:
        server = smtplib.SMTP()
        server.connect(settings.SMTP_SERVER, settings.SMTP_PORT)
        server.login(settings.EMAIL_USER, settings.EMAIL_AUTH_CODE)
        server.sendmail(me, to_mail, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(str(e))
        return False
