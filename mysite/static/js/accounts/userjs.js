/**
 * Created by pandonglin on 2017/1/26.
 */
function DelUser(ths) {
    $.ajax({
        url: '/accounts/user_del/',
        type: 'POST',
        data: {"id": $(ths).parent().parent().attr("id")},
        dataType: 'json',
        success: function(data){
            if(data==204){
                $(ths).parent().parent().remove();
            }else{
                $('#msg-error').text("操作失败")
            }
        }
    });
}

$(function () {
    $('#reset_pwd').on("click", function () {
        $('.msg-error').remove();

        $.ajax({
            url: "/accounts/reset_pwd/",
            type: "POST",
            data: {
                "new_password1": $("form input[name='new_password1']").val().trim(),
                "new_password2": $("form input[name='new_password2']").val().trim()
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
});


$(function () {
    $("#submit_user_add").on("click", function () {
        var data = {};
        var role = [];
        $("form input:text").each(function(){
            data[$(this).attr('name')]=$(this).val().trim();
        });
        $("form input:password").each(function(){
            data[$(this).attr('name')]=$(this).val().trim();
        });
        $(".right_select option").each(function(){
            role.push($(this).val().trim());
        });
        data['role']=role;
        console.log(data);

        $.ajax({
            url: '/accounts/user_add/',
            type: 'POST',
            data: data,
            traditional: true,
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
            data[$(this).attr('name')]=$(this).val().trim();
        });
        $("form input:checkbox").each(function(){
            data[$(this).attr('name')]=$(this).is(":checked");
        });
        $(".right_select option").each(function(){
            role.push($(this).val().trim());
        });
        data['role']=role;
        console.log(data);

        $.ajax({
            url: '/accounts/user_update/' + user_id + '/',
            type: 'POST',
            data: data,
            traditional: true,
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

function DelRole(ths){
    $.ajax({
        url: '/accounts/role_del/',
        type: 'POST',
        data: {"id": $(ths).parent().parent().attr("id")},
        dataType: 'json',
        success: function(data){
            if(data==204){
                $(ths).parent().parent().remove();
            }else{
                $('#msg-error').text("操作失败")
            }
        }
    });
}

$(function () {
    $("#submit_role_add").on("click", function () {
        var data = {};
        var perm = [];
        $("form input:text").each(function(){
            data[$(this).attr('name')]=$(this).val().trim();
        });
        $(".right_select option").each(function(){
            perm.push($(this).val().trim());
        });
        data['perm']=perm;
        console.log(data);

        $.ajax({
            url: '/accounts/role_add/',
            type: 'POST',
            data: data,
            traditional: true,
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
    $("#submit_role_update").on("click", function () {
        var perm = [];
        var role_id = $("form").attr("id");
        $(".right_select option").each(function(){
            perm.push($(this).val());
        });

        $.ajax({
            url: '/accounts/role_update/' + role_id + '/',
            type: 'POST',
            data: {
                'name': $("form input").val().trim(),
                'perm': perm
            },
            traditional: true,
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

function DelPerm(ths){
    $.ajax({
        url: '/accounts/permission_del/',
        type: 'POST',
        data: {"id": $(ths).parent().parent().attr("id")},
        dataType: 'json',
        success: function(data){
            if(data==204){
                $(ths).parent().parent().remove();
            }else{
                $('#msg-error').text("操作失败")
            }
        }
    });
}

$(function () {
    $("#submit_permission_add").on("click", function () {
        var data = {};
        $("form input:text").each(function(){
            data[$(this).attr('name')]=$(this).val().trim();
        });
        console.log(data);

        $.ajax({
            url: '/accounts/permission_add/',
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


var ChangePerm = function (ths) {
    var PermId = $(ths).parent().parent().attr("id");
    $(".row input[name='caption']").val($("#"+PermId+" td:eq(0)").text().trim());
    $(".row input[name='code']").val($("#"+PermId+" td:eq(1)").text().trim());
    $(".row input[name='method']").val($("#"+PermId+" td:eq(2)").text().trim());
    $(".row input[name='kwargs']").val($("#"+PermId+" td:eq(3)").text().trim());
    $(".modal-body").attr("change_id", PermId);
    $(ths).attr("data-target","#myModal");
};

$(function () {
    $(".change_perm").on("click", function () {
        var PermId = $(".modal-body").attr("change_id");
        var data = {};
        $(".modal-body input:text").each(function(){
            data[$(this).attr('name')]=$(this).val().trim().trim();
        });
        console.log(data);

        $.ajax({
            url: '/accounts/permission_update/' + PermId + '/',
            type: 'POST',
            data: data,
            dataType: 'json',
            success: function(data){
                $('.msg-error').remove();
                if(data.status){
                    $(".modal-body").append('<div id="msg-error" class="msg-error">修改成功</div>');
                    $("#"+PermId+" td:eq(0)").text(data.data["caption"]);
                    $("#"+PermId+" td:eq(1)").text(data.data["code"]);
                    $("#"+PermId+" td:eq(2)").text(data.data["method"]);
                    $("#"+PermId+" td:eq(3)").text(data.data["kwargs"]);
                }else{
                    $.each(data.message, function (k, v) {
                        $(".modal-body").append('<div id="msg-error" class="msg-error">'+k+v[0].message+'</div>');
                    })
                }
            }
        })
    })
});

