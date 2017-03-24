/**
 * Created by pandonglin on 2017/1/26.
 */


(function (jq) {

        /*
     CSRF配置
     */
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    /*
     全局Ajax中添加请求头X-CSRFToken，用于跨过CSRF验证
     */
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
            }
        }
    });

    function init() {

        /*
        用户登陆
        */
        $("#loginButton").on("click", function(){
            $('.msg-error').remove();

            var data = {
                'name': $("input[name='name']").val(),
                'password': $("input[name='password']").val()
            };

            $.ajax({
                url: '/accounts/login.html',
                type: 'POST',
                data: data,
                dataType: 'json',

                success: function(data){

                    if (data.status) {
                        window.location.href = '/assets/index.html';
                    } else {
                        $.each(data.message, function (k, v) {
                            var tag = '<span class="msg-error">' + v[0].message + '</span>';
                            $("#" + k ).parent().append(tag);
                            setTimeout(function () {
                                $('.msg-error').remove();
                            }, 3000);
                        })
                    }
                }
            })
        });


        /*
        修改密码
        */

        $('#update_pwd').on("click", function () {
            $('.msg-error').remove();

            $.ajax({
                url: "/accounts/change_pwd.html",
                type: "POST",
                data: {
                    "old_password": $("form input[name='old_password']").val().trim(),
                    "new_password1": $("form input[name='new_password1']").val().trim(),
                    "new_password2": $("form input[name='new_password2']").val().trim()
                },
                dataType: 'json',

                success: function (data) {

                    if (data.status) {
                        window.location.href = '/accounts/login.html';
                    } else {
                        $.each(data.message, function (k, v) {
                            var tag = '<span class="msg-error">' + v[0].message + '</span>';
                            $("#" + k).parent().append(tag);
                        })
                    }
                }
            });
        });


        /*
        密码找回，获取验证码
        */
        $("#get_code").on("click", function(){
            $('.msg-error').remove();

            var email = $("form input[name='email']").val().trim();
            if(email.trim().length == 0){
                var tag = '<span class="msg-error">请输入注册邮箱</span>';
                $("input[name='email']").parent().append(tag);
                return false;
            }
            if($(this).hasClass('btn-default')){
                return false;
            }
            var ths = $(this);
            var time = 59;

            var remindLabel = '<div class="col-sm-offset-4" style="color: red;">请在5分钟内使用验证码</div>';
            $('form').append(remindLabel);

            $.ajax({
                url: "/accounts/send_msg.html",
                type: 'POST',
                data: {"email": email},
                dataType: 'json',

                success: function(data){

                    if (data.status){
                       $('#forget_pwd').removeClass('btn-default').addClass('btn-success');
                        ths.addClass('btn-default');
                        var interval = setInterval(function(){
                            ths.text("已发送(" + time + ")");
                            if(time <= 0){
                                clearInterval(interval);
                                ths.removeClass('btn-default');
                                ths.text("获取验证码");
                                }
                            time -= 1;
                        }, 1000);
                    } else {
                        var tag = "<span class='msg-error'>" + data.message + "</span>";
                        $("input[name='email']").parent().append(tag);
                    }
                }
            });
        });


        /*
        密码找回，提交数据
        */

        $('#forget_pwd').on("click", function () {
            $('.msg-error').remove();
            if ($(this).hasClass("btn-success")){

                $.ajax({
                    url: "/accounts/forget_pwd.html",
                    type: "POST",
                    data: {
                        "email": $("form input[name='email']").val().trim(),
                        "code": $("form input[name='code']").val().trim()
                    },
                    dataType: 'json',

                    success: function (data) {

                        if (data.status) {
                            window.location.href = '/accounts/reset_pwd.html';
                        } else {
                            $.each(data.message, function (k, v) {
                                var tag = '<span class="msg-error">' + v[0].message + '</span>';
                                $("#" + k).parent().append(tag);
                            })
                        }
                    }
                });
            } else {
                var tag = '<span class="msg-error">邮箱和验证码为必填项</span>';
                $("#code").parent().append(tag);
            }
        });



        /*
         重设密码
         */
        $('#reset_pwd').on("click", function () {
            $('.msg-error').remove();

            $.ajax({
                url: "/accounts/reset_pwd.html",
                type: "POST",
                data: {
                    "new_password1": $("form input[name='new_password1']").val().trim(),
                    "new_password2": $("form input[name='new_password2']").val().trim()
                },
                dataType: 'json',

                success: function (data) {
                    if (data.status) {
                        window.location.href = '/accounts/login.html';
                    } else {
                        $.each(data.message, function (k, v) {
                            var tag = '<span class="msg-error">' + v[0].message + '</span>';
                            $("#" + k).parent().append(tag);
                        })
                    }
                }
            });
        });


        /*
         添加用户
         */
        $("#submit_user_add").on("click", function () {
            $('.msg-error').remove();

            var data = {};
            var role = [];

            $("form input:text").each(function () {
                data[$(this).attr('name')] = $(this).val().trim();
            });

            $("form input:password").each(function () {
                data[$(this).attr('name')] = $(this).val().trim();
            });

            $(".single_select").each(function () {
                data[$(this).attr('name')] = $(this).val().trim();
            });

            $(".right_select option").each(function () {
                role.push($(this).val().trim());
            });
            data['role'] = role;
            console.log(data);

            $.ajax({
                url: '/accounts/user_add.html',
                type: 'POST',
                data: data,
                traditional: true,
                dataType: 'json',

                success: function (data) {
                    if (data.status) {
                        var tag = '<div class="form-group"><div class="col-sm-4 col-sm-offset-6"><div class="msg-error">添加成功</div></div></div>';
                        $('.hr-line-dashed').after(tag);

                        setTimeout(function () {
                            $('.msg-error').remove();
                        }, 5000);
                    } else {
                        $.each(data.message, function (k, v) {
                            // console.log(v[0].message);
                            var tag = '<span class="msg-error">' + v[0].message + '</span>';
                            $("#" + k).parent().append(tag);
                        })
                    }
                }
            })
        });

    }

    /*
     更新权限
     */

    function updatePermButton(ths) {
        $('.msg-error').remove();
        var PermId = $(ths).parent().parent().attr("id");
        $(".modal-body input[name='caption']").val($("#" + PermId + " td:eq(1)").text().trim());
        $(".modal-body input[name='code']").val($("#" + PermId + " td:eq(2)").text().trim());
        $(".modal-body input[name='method']").val($("#" + PermId + " td:eq(3)").text().trim());
        $(".modal-body input[name='kwargs']").val($("#" + PermId + " td:eq(4)").text().trim());
        $(".modal-body").attr("permId", PermId);
        $(ths).attr("data-target", "#myModal");
    }


    /*
    绑定权限提交事件
    */
    function bingPermButton() {
        $(".changePerm").on("click", function () {
            $('.msg-error').remove();

            var data = {};
            var PermId = $(".modal-body").attr("permId");
            $(".modal-body input:text").each(function () {
                data[$(this).attr('name')] = $(this).val().trim();
            });

            console.log(data);

            $.ajax({
                url: '/accounts/permission_update.html?id=' + PermId,
                type: 'POST',
                data: data,
                dataType: 'JSON',
                traditional: true,

                success: function (data) {

                    if (data.status) {
                        $(".modal-body").append('<div id="msg-error" class="msg-error">修改成功</div>');
                        $("#" + PermId + " td:eq(1)").text(data.data["caption"]);
                        $("#" + PermId + " td:eq(2)").text(data.data["code"]);
                        $("#" + PermId + " td:eq(3)").text(data.data["method"]);
                        $("#" + PermId + " td:eq(4)").text(data.data["kwargs"]);
                    } else {
                        $.each(data.message, function (k, v) {
                            $(".modal-body").append('<div id="msg-error" class="msg-error">' + k + v[0].message + '</div>');
                        })
                    }
                }
            })
        })
        }

    jq.extend({
        'userJsInit': function () {
            init();
            bingPermButton();
        },
        'updatePermButton': function (ths) {
            updatePermButton(ths);
        }
    })

})(jQuery);

$.userJsInit();
