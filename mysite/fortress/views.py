from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect, HttpResponse, get_object_or_404

# Create your views here.


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
    return render(request, 'fortress/show_message.html')