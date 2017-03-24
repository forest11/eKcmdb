#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __Author__: PanDongLin
import pymysql
from backend.sqlcheck import sqlconfig


class Inception(object):
    def __init__(self):
        try:
            self.in_host = getattr(sqlconfig, 'IN_HOST')
            self.in_port = int(getattr(sqlconfig, 'IN_PORT'))
            self.host = getattr(sqlconfig, 'DB_HOST')
            self.port = int(getattr(sqlconfig, 'DB_PORT'))
            self.db_user = getattr(sqlconfig, 'DB_USER')
            self.db_passwd = getattr(sqlconfig, 'DB_PWD')
            self.db_name = getattr(sqlconfig, 'DB_NAME')
        except Exception as e:
            print("Error: %s" % str(e))

    def sqlauto_review(self, sql_str):
        """
        将sql交给inception进行自动审核，并返回审核结果
        :param sql_str:
        :return:
        """
        sql = """/*--user=%s;--password=%s;--host=%s;--enable-check=1;--port=%s;*/
        inception_magic_start;
        use %s;
        set names utf8;
        %s
        inception_magic_commit;
        """ % (self.db_user, self.db_passwd, self.host, self.port, self.db_name, sql_str)
        result = self._fetchall(sql, self.in_host, self.in_port, '', '', '')
        return result

    def _fetchall(self, sql, host, port, user, password, dbname):
        """
        封装mysql连接和获取结果集方法
        :param sql: 执行语句
        :param host: 主机ip
        :param port: 主机端口
        :param user: 连接数据库用户
        :param password: 用户密码
        :param dataname: 数据库名
        :return:
        """
        try:
            conn = pymysql.connect(host=host, port=port, user=user, passwd=password, db=dbname, charset='utf8')
            cursor = conn.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
        except Exception as e:
            result = str(e)
        finally:
            cursor.close()
            conn.close()
            return result

