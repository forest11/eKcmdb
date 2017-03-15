import paramiko
from database import models


def ssh_host_exec_cmd(auth_type, host_ip, host_port, user, passwd_or_key, cmd, *args, **kwargs):
    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 自动应答
    try:
        if auth_type == 0:  # 0表示为通过密码认证
            s.connect(host_ip, host_port, user, passwd_or_key, timeout=5)
        else:
            # RSA_PRIVATE_KEY_FILE为key的文件路径
            key = paramiko.RSAKey.from_private_key_file('RSA_PRIVATE_KEY_FILE')
            s.connect(host_ip, host_port, user, pkey=passwd_or_key, timeout=5)
        if isinstance(args, str):
            cmd = "%s %s" % (cmd, args)
        elif isinstance(args, list):
            tmp_args = " ".join(args)
            cmd = "%s %s " % (cmd, tmp_args)

        stdin, stdout, stderr = s.exec_command(cmd)
        result = stdout.read(), stderr.read()
        if any(result):
            cmd_result = result[0] if result[0] else result[1]
        else:
            cmd_result = b'no output!'

        status = 1
        print('-----------  IP:%s -------------' % host_ip)
    except Exception as e:
        print('\033[31;1mError:%s\033[0m' % str(e))
        cmd_result = str(e)
        status = 2
    s.close()
    return cmd_result, status


def exec_cmd(task_id, bind_host_id, cmd,  *args, **kwargs):
    bind_host = models.BindHost.objects.get(id=bind_host_id)  # 取出远程主机对象
    cmd_result, exec_status = ssh_host_exec_cmd(bind_host.remote_user.auth_type,
                                                bind_host.host.ip,
                                                int(bind_host.port),
                                                bind_host.remote_user.username,
                                                bind_host.remote_user.password,
                                                cmd,
                                                *args,
                                                **kwargs)

    log_obj = models.TaskDetail.objects.get(bing_task_id=int(task_id), bind_host_id=bind_host.id)  # 记录日志
    log_obj.event_log = cmd_result
    log_obj.exec_status = exec_status
    log_obj.save()
