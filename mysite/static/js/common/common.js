/**
 * Created by pandonglin on 2017/1/15.
 */
var AddBusiness = function() {
    $("#submit_business_add").on("click", function(){
        var data = {};
        data = {"name": $("#name").val(),
                "service": "1",
                "memo": $("#memo").val()};
        console.log(data);
        $.ajax({
            url: '/common/business_add/',
            type: 'POST',
            data: data,
            dataType: 'json',
            success: function(data){
                $('.msg-error').remove();
                if(data.status){
                    var tag = '<div class="col-sm-4 col-sm-offset-5"><span class="msg-error">添加成功</span></div>';
                    $('#submit_business_add').parent().parent().append(tag);
                }else{
                    $.each(data.message, function (k, v) {
                        var tag = '<span class="msg-error">'+v[0].message+'</span>';
                        $("#"+ k).parent().append(tag);
                    })
                }
            }
        })
    })
};

var AddService = function() {
    $("#submit_service_add").on("click", function(){
        var data = {};
        data = {"name": $("#name").val(),
                "port": $("#port").val(),
                "host": "1",
                "memo": $("#memo").val()};
        console.log(data);
        $.ajax({
            url: '/common/service_add/',
            type: 'POST',
            data: data,
            dataType: 'json',
            success: function(data){
                $('.msg-error').remove();
                if(data.status){
                    var tag = '<div class="col-sm-4 col-sm-offset-5"><span class="msg-error">添加成功</span></div>';
                    $('#submit_service_add').parent().parent().append(tag);
                }else{
                    $.each(data.message, function (k, v) {
                        var tag = '<span class="msg-error">'+v[0].message+'</span>';
                        $("#"+ k).parent().append(tag);
                    })
                }
            }
        })
    })
};

AddBusiness();
AddService();