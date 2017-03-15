from database import models
from backend.devops import run_cmd


class TaskHander(object):
    def __init__(self, request):
        self.request = request
        self.errors = []
        self.task_data = {}

    def task_parser(self):
        if self.request.POST.get('action'):
            self.task_data['action'] = self.request.POST.get('action')
        else:
            self.errors.append({'msg-error': '未指定操作方式'})

        if self.request.POST.getlist('selected_bind_hosts'):
            bind_hosts = set(self.request.POST.getlist('selected_bind_hosts'))
            selected_bind_hosts = models.BindHost.objects.filter(id__in=bind_hosts)
            if selected_bind_hosts:
                self.task_data['bind_hosts'] = selected_bind_hosts
            else:
                self.errors.append({'msg-error': '选中主机无法连接'})
        else:
            self.errors.append({'msg-error': '未选中需要执行主机'})

        if self.request.POST.get('cmd'):
            self.task_data['cmd'] = self.request.POST.get('cmd')
        else:
            self.errors.append({'msg-error': '未输入操作指令'})

    def is_valid(self):
        self.task_parser()
        if self.errors:
            return False
        return True

    def exec_cmd(self, task_id, bind_host_list, cmd):
        for host in bind_host_list:
            run_cmd.exec_cmd(task_id, host.id, cmd)

    def start(self):
        task_obj = models.Task(
            task_type=self.task_data['action'],
            user=self.request.user,
            cmd=self.task_data['cmd']
        )
        task_obj.save()
        task_obj.bind_hosts.add(*self.task_data['bind_hosts'])

        task_obj_list = []
        for bind_host in task_obj.bind_hosts.select_related():
            task_obj_list.append(
                models.TaskDetail(
                    bing_task=task_obj,
                    bind_host=bind_host,
                    exec_status=3
                )
            )
        models.TaskDetail.objects.bulk_create(task_obj_list)
        self.task = task_obj
        self.exec_cmd(self.task.id, self.task_data['bind_hosts'], self.task_data['cmd'])

