/**
 * Created by pandonglin on 2017/3/14.
 */

(function (jq) {


    /*
     当前页面的url
     */
    var requestUrl;


    /*页面初始化*/
    function init() {
        banNextButton();
        submitData();
    }


    /*
     禁用下一页按钮
     */
    function banNextButton() {
        var nextButton = $('#next');
        var Li = nextButton.parent();
        nextButton.attr('href', '#');
        Li.attr('aria-disabled', 'true').attr('class', 'disabled');
    }


    /*
     启用下一页按钮
     */
    function freeNextButton() {
        var nextButton = $('#next');
        var Li = nextButton.parent();
        nextButton.attr('href', '#next');
        Li.attr('aria-disabled', 'false').attr('class', 'true');
    }


    /*
     完成按钮，启动下一页按钮
     */
    function doNext(ths) {
        freeNextButton();
    }


    /*
     提交数据
     */
    function submitData() {

        $("#exec_button").on("click", function () {
            $('#sql-result').children().remove();
            var dy = '<div class="sk-spinner sk-spinner-three-bounce __web-inspector-hide-shortcut__"> <div class="sk-bounce1"></div><div class="sk-bounce2"></div><div class="sk-bounce3"></div> </div>'
            $("#sql-result").append(dy);

            var data = {};

            $("form input:text").each(function () {
                data[$(this).attr('name')] = $(this).val().trim();
            });

            $("form select").each(function () {
                data[$(this).attr('name')] = $(this).val();
            });

            $("form input:checkbox").each(function () {
                data[$(this).attr('name')] = $(this).is(':checked');
            });

            $("form textarea").each(function () {
                data[$(this).attr('name')] = $(this).val().trim();
            });

            var mulSelect = $('.right_select').attr('name');

            data[mulSelect] = [];
            $(".right_select option").each(function () {
                data[mulSelect].push($(this).val());
            });
            console.log(data);

            $.ajax({
                url: requestUrl,
                type: 'POST',
                data: data,
                dataType: 'json',
                traditional: true,

                success: function (response) {
                    $("#sql-result").empty();
                    if (response.status) {
                        var tag = '<span class="control-label col-sm-2">执行结果:</span><div class="col-sm-9"><textarea class="form-control" rows="25" type="text">' + response.data + '</textarea></div>';
                        $("#sql-result").append(tag);
                    } else {
                        alert("加载数据错误。。。");
                    }
                }
            })
        })
    }


    /*
     host被选中计数器
     */
    function AddCounter(ths) {
        var current_count = parseInt($(".selected_host_count").text());
        if ($(ths).prop("checked") == true) {
            //没选中数量+1，选中再次点击，数量减1
            $(".selected_host_count").text(current_count + 1);
        } else {
            $(".selected_host_count").text(current_count - 1);
        }
    }

    /*
     获取执行结果
     */
    function GetTaskResult(task_id) {
        $('#task_result').text('');
        $.ajax({
            url: '/devops/task_center/result/',
            type: 'GET',
            data: {task_id: task_id},
            dataType: 'json',
            traditional: true,
            success: function (response) {
                $.each(response, function (index, ths) {
                    var single_res = "";
                    var ret;
                    if (ths.exec_status == 0) {
                        ret = '正在执行';
                    } else if (ths.exec_status == 1) {
                        ret = '执行成功';
                    } else if (ths.exec_status == 2) {
                        ret = '执行失败';
                    } else if (ths.exec_status == 3) {
                        ret = '未知';
                    }
                    single_res += "<h4>Host:  " + ths.bind_host__host__hostname + " 执行状态:" + ret + "</h4>";
                    single_res += "<pre> " + ths.event_log + "</pre>";  //原文本显示

                    $("#task_result").append(single_res);
                });
            },
            error: function () {
                alert('请求异常');
            }
        });
    }


    /*
     提交数据
     */
    function PostTask() {
        var selected_hosts = $(".bind_host_list input:checked");
        var selected_bind_hosts = [];

        $.each(selected_hosts, function (index, ths) {
            selected_bind_hosts.push(ths.value);
        });
        if (selected_bind_hosts.length == 0) {
            alert("当前无选中主机");
            return;
        }
        var cmd = $("#cmd").val().trim();
        if (cmd.length == 0) {
            alert("无命令可执行");
            return;
        }

        var dy = '<div class="sk-spinner sk-spinner-three-bounce __web-inspector-hide-shortcut__"> <div class="sk-bounce1"></div><div class="sk-bounce2"></div><div class="sk-bounce3"></div> </div>'
        $("#task_result").append(dy);
        var task_data = {
            'action': 0,
            'cmd': cmd,
            'selected_bind_hosts': selected_bind_hosts
        };

        $.ajax({
            url: '/devops/task_center.html',
            type: 'POST',
            data: task_data,
            dataType: 'json',
            traditional: true,
            success: function (response) {
                $("#task_result").empty();
                if (response.task_id) {
                    GetTaskResult(response.task_id);
                } else {
                    var single_res = "";
                    single_res += "<pre> " + response.errors + "</pre>";
                    $("#task_result").append(single_res);
                }
            },
            error: function () {
                alert('数据异常');
            }
        });
    }

    jq.extend({
        'devOpsInit': function (url) {
            requestUrl = url;
            init();
        },
        'devOpsDoNext': function (ths) {
            doNext(ths);
        },
        'pushSql': function () {
            checkSqlFun();
        },
        'AddCounter': function (ths) {
            AddCounter(ths);
        },
        'PostTask': function () {
            PostTask();
        }
    })

})(jQuery);