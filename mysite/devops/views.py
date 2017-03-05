import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse
from devops import models, task_handle


@login_required
def show_message(request):
    """
    用于跳板机登陆认证，暂未使用
    :param request:
    :return:
    """
    if request.method == 'POST':
        msg = request.POST.get("msg", "")
        msg_list = msg.split("-")
        #输入不为空，分割后为int类型数据，以及所有值不能大于user_key的长度
        if msg_list and all([i.isdigit() for i in msg_list]) and all([int(i) < len(request.user.user_key) for i in msg_list]):
            ret = [request.user.user_key[int(i)] for i in msg_list]
        else:
            ret = "输入错误"
        return HttpResponse(ret)
    return render(request, 'devops/show_message.html')


def json_date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.strftime("%Y-%m-%d %T")


def multi_cmd(request):
    return render(request, 'devops/multi_cmd.html')


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


def code_commit(request):
    return render(request, 'common/index.html')


def code_audit(request):
    return render(request, 'common/index.html')


def code_list(request):
    return render(request, 'devops/code_list.html', locals())