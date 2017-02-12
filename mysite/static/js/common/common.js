/**
 * Created by pandonglin on 2017/1/15.
 */
$(function() {
    $("#submit_business_add").on("click", function(){
        var service = [];
        $(".right_select option").each(function(){
            service.push($(this).val().trim());
        });
        var data = {"name": $("#name").val().trim(),
                    "service": service,
                    "memo": $("#memo").val().trim()};
        console.log(data);

        $.ajax({
            url: '/common/business_add/',
            type: 'POST',
            data: data,
            traditional: true,
            dataType: 'json',
            success: function(data){
                $('.msg-error').remove();
                if(data.status){
                    var tag = '<div class="col-sm-offset-4"><div class="msg-error">添加成功</div></div>';
                    $('form').append(tag);
                }else{
                    $.each(data.message, function (k, v) {
                        var tag = '<span class="msg-error">'+v[0].message+'</span>';
                        $("#"+ k).parent().append(tag);
                    })
                }
            }
        })
    })
});


$(function () {
    $("#submit_business_update").on("click", function () {
        var service = [];
        $(".right_select option").each(function(){
            service.push($(this).val().trim());
        });
        var data = {"name": $("#name").val().trim(),
                    "service": service,
                    "memo": $("#memo").val().trim()};
        console.log(data);

        $.ajax({
            url: '/common/business_update/' + $("form").attr("id")  + '/',
            type: 'POST',
            data: data,
            traditional: true,
            dataType: 'json',
            success: function(data){
                $('.msg-error').remove();
                if(data.status){
                    var tag = '<div class="col-sm-offset-4"><div class="msg-error">添加成功</div></div>';
                    $('form').append(tag);
                }else{
                    $.each(data.message, function (k, v) {
                        var tag = '<span class="msg-error">'+v[0].message+'</span>';
                        $("#"+ k).parent().append(tag);
                    })
                }
            }
        })
    })
});


function DelBus(ths) {
    $.ajax({
        url: '/common/business_del/',
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

$(function() {
    $("#submit_service_add").on("click", function(){
        var host = [];
        $(".right_select option").each(function(){
            host.push($(this).val().trim());
        });
        var data = {"name": $("#name").val().trim(),
                    "port": $("#port").val().trim(),
                    "host": host,
                    "memo": $("#memo").val().trim()};
        console.log(data);
        $.ajax({
            url: '/common/service_add/',
            type: 'POST',
            data: data,
            traditional: true,
            dataType: 'json',
            success: function(data){
                $('.msg-error').remove();
                if(data.status){
                    var tag = '<div class="col-sm-offset-4"><div class="msg-error">添加成功</div></div>';
                    $('form').append(tag);
                }else{
                    $.each(data.message, function (k, v) {
                        var tag = '<span class="msg-error">'+v[0].message+'</span>';
                        $("#"+ k).parent().append(tag);
                    })
                }
            }
        })
    })
});


function DelSer(ths) {
    $.ajax({
        url: '/common/service_del/',
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
    $("#submit_service_update").on("click", function () {
        var host = [];
        $(".right_select option").each(function(){
            host.push($(this).val().trim());
        });
        var data = {"name": $("#name").val().trim(),
                    "port": $("#port").val().trim(),
                    "host": host,
                    "memo": $("#memo").val().trim()};
        console.log(data);
        $.ajax({
            url: '/common/service_update/' + $("form").attr("id") + '/',
            type: 'POST',
            data: data,
            traditional: true,
            dataType: 'json',
            success: function(data){
                $('.msg-error').remove();
                if(data.status){
                    var tag = '<div class="col-sm-offset-4"><div class="msg-error">修改成功</div></div>';
                    $('form').append(tag);
                }else{
                    $.each(data.message, function (k, v) {
                        var tag = '<span class="msg-error">'+v[0].message+'</span>';
                        $("#"+ k).parent().append(tag);
                    })
                }
            }
        })
    });
});


$(function () {
    $("#left_mv").on("click", function () {
        $(".left_select option:selected").each(function(){
            var tag = "<option value="+$(this).val()+">"+$(this).text()+"</option>";
            $(".right_select").append(tag);
            $(this).remove();
        });
    });
    $("#right-mv").on("click", function () {
        $(".right_select option:selected").each(function(){
            var tag = "<option value="+$(this).val()+">"+$(this).text()+"</option>";
            $(".left_select").append(tag);
            $(this).remove();
        });
    })
});