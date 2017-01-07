from django.shortcuts import render, HttpResponse
from autoops import models, task_handle
import json


def json_date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.strftime("%Y-%m-%d %T")


def multi_cmd(request):
    return render(request, 'autoops/multi_cmd.html')


def task_center(request):
    if request.method == "POST":
        selected_bind_hosts = request.POST.getlist("selected_bind_hosts")
        print("task", selected_bind_hosts)
        task_obj = task_handle.TaskHander(request)
        if task_obj.is_valid():
            task_obj.start()
            # response = {'task_id': task_obj.task.id}
            response = {'task_id': 1}
        else:
            response = {'errors': task_obj.errors}
        return HttpResponse(json.dumps(response))


def get_task_result(request):
    task_id = request.GET.get('task_id')
    task_result = models.TaskDetail.objects.filter(task_id=task_id).values('result', 'id', 'event_log', 'bind_host__host__hostname', 'bind_host__remote_user__username')
    task_result_list = list(task_result)
    # return HttpResponse(json.dumps(task_result, default=json_date_handler))
    return HttpResponse(json.dumps(task_result_list))