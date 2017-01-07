/**
 * Created by Administrator on 2016/12/8.
 */
var Login = function() {
    var handleLogin = function() {
        $("button").on("click", function(){
            var data = {
                'email': $("input[name='email']").val(),
                'password': $("input[name='password']").val()
            };
            $.ajax({
                url: '/accounts/login/',
                type: 'POST',
                data: data,
                dataType: 'json',
                success: function(data){
                    if (!data.status){
                        console.log(data.status);
                        console.log(data.message);
                    }
                }
            })
        })
    };

    return {
        init: function() {
            handleLogin();
        }
    };
}();


var SendMsg = function(){
        $("#get_code").click(function(){
            $('.msg-error').remove();
            var email = $("input[name='email']").val();
            if(email.trim().length == 0){
                var tag = '<span class="msg-error">请输入注册邮箱</span>';
                $("input[name='email']").parent().append(tag);
                return;
            }
            if($(this).hasClass('sending')){
                return;
            }
            var ths = $(this);
            var time = 59;

            $.ajax({
                url: "/accounts/send_msg/",
                type: 'POST',
                data: {"email": email},
                dataType: 'json',
                success: function(data){
                    if(!data.status){
                        var tag = "<span class='msg-error'>"+data.summary+"</span>";
                        $("input[name='email']").parent().append(tag);
                    }else{
                        ths.addClass('sending btn-warning');
                        var interval = setInterval(function(){
                            ths.text("已发送(" + time + ")");
                            if(time <= 0){
                                clearInterval(interval);
                                ths.removeClass('sending btn-warning');
                                ths.text("获取验证码");
                                }
                            time -= 1;
                        }, 1000);
                    }
                }
            });
        });
 };

var ResetPwd = function () {
    $('#resetpwd').click(function () {
        $('.msg-error').remove();

        $.ajax({
            url: "/accounts/reset_pwd/",
            type: "POST",
            data: {
                "new_password1": $("input[name='new_password1']").val(),
                "new_password2": $("input[name='new_password2']").val()
            },
            dataType: 'json',
            success: function (data) {
                if(data.status){
                    window.location.href = '/accounts/login/';
                }else{
                    $.each(data.message, function (k, v) {
                        var tag = '<span class="msg-error">'+v[0].message+'</span>';
                        $("#"+k).parent().append(tag);
                    })
                }
            }
        });
    });
};

