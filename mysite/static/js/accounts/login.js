/**
 * Created by Administrator on 2016/12/8.
 */
$(function() {
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
});


$(function(){
    $("#get_code").on("click", function(){
        $('.msg-error').remove();
        var email = $("form input[name='email']").val();
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
 });



