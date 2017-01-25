from autoops import models


class TaskHander(object):
    def __init__(self, request):
        self.request = request
        self.errors = []
        self.task_data = {}

    def task_parser(self):
        if self.request.POST.get('action'):
            self.task_data['action'] = self.request.POST.get('action')
        else:
            self.errors.append({'lack_argument': 'task action is not provided'})
        if self.request.POST.getlist('selected_bind_hosts'):
            self.task_data['bind_hosts'] = set(self.request.POST.getlist('selected_bind_hosts'))
        else:
            self.errors.append({'lack_argument': 'selected_bind_hosts is not provided'})

        if self.request.POST.get('cmd'):
            self.task_data['cmd'] = self.request.POST.get('cmd')
        else:
            self.errors.append({'lack_argument': 'cmd is not provided'})

    def is_valid(self):
        self.task_parser()
        if self.errors:
            return False
        return True

    def start(self):
        print("validations passed...going to run task...")
        task_obj = models.Task(
            task_type=self.task_data['action'],
            user=self.request.user,
            #bind_hosts= models.BindHost.objects.filter(id__in = self.task_data['bind_hosts']),
            task_detail=self.task_data['cmd']
        )
        task_obj.save()
        task_obj.bind_hosts.add(*self.task_data['bind_hosts'])

        task_detail_objs = []
        for bind_host in task_obj.bind_hosts.select_related():
            task_detail_objs.append(
                models.TaskDetail(
                    task=task_obj,
                    bind_host=bind_host,
                    result=2
                )
            )
        models.TaskDetail.objects.bulk_create(task_detail_objs)
        self.task = task_obj
        #print("--task_obj->",task_obj)
