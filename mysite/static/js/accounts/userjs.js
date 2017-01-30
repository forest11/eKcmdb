/**
 * Created by pandonglin on 2017/1/26.
 */
function DelUser(ths) {
    $.ajax({
        url: '/accounts/user_del/',
        type: 'POST',
        data: {"id": $(ths).attr("id")},
        dataType: 'json',
        success: function(data){
            if(data==204){
                $(ths).parent().parent().remove();
            }else{
                $('#msg-error').val("操作失败")
            }
        }
    });
}

var ResetPwd = function () {
    $('#resetpwd').on("click", function () {
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

$(function () {
    $("#submit_user_add").on("click", function () {
        var data = {};
        var role = [];
        $("form input:text").each(function(){
            data[$(this).attr('name')]=$(this).val();
        });
        $("form input:password").each(function(){
            data[$(this).attr('name')]=$(this).val();
        });
        $("#right_select option").each(function(){
            role.push($(this).val());
        });
        data['role']=role;
        console.log(data);

        $.ajax({
            url: '/accounts/user_add/',
            type: 'POST',
            data: data,
            dataType: 'json',
            success: function(data){
                $('.msg-error').remove();
                if(data.status){
                    var tag = '<div class="col-sm-offset-4"><div class="msg-error">添加成功</div></div>';
                    $('form').append(tag);
                }else {
                    $.each(data.message, function (k, v) {
                       // console.log(v[0].message);
                       var tag = '<span class="msg-error">' + v[0].message + '</span>';
                       $("#"+ k).parent().append(tag);
                    })
                }
            }
        })
    })
});

$(function () {
    $("#submit_user_update").on("click", function () {
        var data = {};
        var role = [];
        var user_id = $("form").attr("id");
        $("form input:text").each(function(){
            data[$(this).attr('name')]=$(this).val();
        });
        $("form input:checkbox").each(function(){
            data[$(this).attr('name')]=$(this).is(":checked");
        });
        $("form input:password").each(function(){
            data[$(this).attr('name')]=$(this).val();
        });
        $("#right_select option").each(function(){
            role.push($(this).val());
        });
        data['role']=role;
        console.log(data);

        $.ajax({
            url: '/accounts/user_update/' + user_id + '/',
            type: 'POST',
            data: data,
            dataType: 'json',
            success: function(data){
                $('.msg-error').remove();
                if(data.status){
                    var tag = '<div class="col-sm-offset-4"><div class="msg-error">修改成功</div></div>';
                    $('form').append(tag);
                }else {
                    $.each(data.message, function (k, v) {
                       // console.log(v[0].message);
                       var tag = '<span class="msg-error">' + v[0].message + '</span>';
                       $("#"+ k).parent().append(tag);
                    })
                }
            }
        })
    })
});