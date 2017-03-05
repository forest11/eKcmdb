import subprocess
import random
import string
import getpass
from django.contrib.auth import authenticate
from devops import models
from mysite import settings


class InteractiveHandler(object):
    '''负责与用户在命令行端所有的交互'''
    def __init__(self,*args,**kwargs):
        if self.authenticate():
            self.interactive()

    def authenticate(self):
        '''用户认证'''
        retry_count = 0
        while retry_count < 3:
            username = input("Username:").strip()
            if len(username)==0:continue
            password = getpass.getpass("Password:")
            user = authenticate(username=username,password=password)
            if user is not None:
                print("\033[32;1mwelcome %s\033[0m".center(50,'-') % user)
                self.user = user
                return True
            else:
                print("wrong username or password!")
                retry_count += 1
        else:
            exit("too many attempts.")

    def create_session(self,bind_host_obj,random_tag):
        session_obj = models.SessionRecord(
            user=self.user,
            bind_host = bind_host_obj,
            rand_tag = random_tag
        )
        session_obj.save()
        return session_obj

    def select_hosts(self,bind_host_list):
        #exit_flag = False
        while True:
            #bind_host_list = host_groups[user_choice].bind_hosts.select_related()
            for index, host_obj in enumerate(bind_host_list):
                print("%s.\t%s" % (index, host_obj))

            user_choice2 = input("[%s]>>>" % self.user).strip()
            if user_choice2.isdigit():
                user_choice2 = int(user_choice2)
                if user_choice2 >= 0 and user_choice2 < len(bind_host_list):
                    bind_host_obj = bind_host_list[user_choice2]
                    
                    random_tag = ''.join(random.sample(string.ascii_lowercase,14))
                    print('random tag:',random_tag)
                    # session_obj = self.create_session(bind_host_obj,random_tag)
                    # cmd_str = "sh %s %s %s " % (settings.SESSION_TRACK_SCRIPT,session_obj.id,session_obj.rand_tag)
                    # print("tracking...",cmd_str)
                    #subprocess.run()


                    cmd = "sshpass -p %s /usr/local/openssh7/bin/ssh %s@%s -p%s  -o StrictHostKeyChecking=no -Z %s" %(bind_host_obj.remote_user.password,
                                             bind_host_obj.remote_user.username,
                                             bind_host_obj.host.ip_addr,
                                             bind_host_obj.host.port,
                                             random_tag)

                    subprocess.run(cmd,shell=True)
                    print('----logout---')
            else:
                if user_choice2 == 'b':
                    break
                if user_choice2 == 'exit':
                    exit("bye")

    def  interactive(self):
        '''用户SHELL'''

        exit_flag = False
        while not exit_flag:
            try:
                host_groups = self.user.g.all()
                print("u.\t未分组[%s]" % self.user.h.all().count())
                for index, group_obj in enumerate(host_groups):
                    print("%s.\t%s组[%s]" %(index, group_obj, group_obj.bind_hosts.all().count()))

                user_choice = input("[%s]>>>"%self.user).strip()
                if len(user_choice) == 0:
                    continue
                if user_choice.isdigit():
                    user_choice = int(user_choice)
                    if user_choice >= 0 and user_choice < len(host_groups):
                        self.select_hosts(host_groups[user_choice].bind_hosts.all())

                else:
                    if user_choice == 'u':
                        try:
                            self.select_hosts(self.user.bind_hosts.all())
                        except AttributeError:
                            print("无效错误...")

                    if user_choice == 'q' or user_choice == 'exit' or user_choice == 'quit':
                        exit("exit")
            except KeyboardInterrupt as e:
                pass
