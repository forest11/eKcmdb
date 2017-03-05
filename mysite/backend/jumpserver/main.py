#!/usr/bin/env python3
# -*— coding: utf-8 -*-
# __author__ : pandonglin

from backend.jumpserver import interactive


class ManagementUtily(object):
    '''分发用户命令'''
    def __init__(self,sys_args):
        self.sys_args = sys_args
        self.argv_verify() #验证并调用用户指令对应的功能

    def show_help_msg(self):
        print('''
            run     启动堡垒机用户终端
        ''')
        exit()

    def argv_verify(self):
        if len(self.sys_args) < 2:
            self.show_help_msg()
        if hasattr(self,self.sys_args[1]):
            func = getattr(self,self.sys_args[1])
            func(self.sys_args)
        else:
            self.show_help_msg()

    def run(self,*args,**kwargs):
        '''启动用户交互程序'''
        interactive.InteractiveHandler(*args,**kwargs)