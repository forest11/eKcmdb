/**
 * Created by Administrator on 2016/12/15.
 */
var AddHost = function() {
    $("#reset_host_add").on("click", function(){
        window.location.reload();
    });

    $("#submit_host_add").on("click", function(){
        var data = {};
        $("form input:text").each(function(){
            data[$(this).attr('name')]=$(this).val();
        });
        $("form select").each(function(){
            data[$(this).attr('name')]=$(this).val();
        });
        $("form input:checkbox").each(function () {
            data[$(this).attr('name')]=$(this).is(':checked');
        });
        $("form textarea").each(function () {
            data[$(this).attr('name')]=$(this).val();
        });
        console.log(data);
        $.ajax({
            url: '/assets/host_add/',
            type: 'POST',
            data: data,
            dataType: 'json',
            success: function(data){
                $('.msg-error').remove();
                if(data.status){
                    var tag = '<div class="col-sm-4 col-sm-offset-5"><span class="msg-error">添加成功</span></div>';
                    $('#submit_host_add').parent().parent().append(tag);
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

var EditHost = function () {
    $("#submit_host_edit").on("click", function(){
        var data = {"id": 1};
        $("form input:text").each(function(){
            data[$(this).attr('name')]=$(this).val();
        });
        $("form select").each(function(){
            data[$(this).attr('name')]=$(this).val();
        });
        $("form input:checkbox").each(function () {
            data[$(this).attr('name')]=$(this).is(':checked');
        });
        $("form textarea").each(function () {
            data[$(this).attr('name')]=$(this).val();
        });
        console.log(data);
        $.ajax({
            url: '/assets/host_edit/',
            type: 'POST',
            data: data,
            dataType: 'json',
            success: function(data){
                console.log(data);
                $('.msg-error').remove();
                if(data.status){
                    var tag = '<div class="col-sm-4 col-sm-offset-5"><span class="msg-error">修改成功</span></div>';
                    $('#submit_host_edit').parent().parent().append(tag);
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
};

function change_info(ths) {
    var data = $(ths).attr("name") + "=" + $(ths).val();
    var IframeUrl = $("#ifrID").attr("src");
    if(IframeUrl.endsWith("iframe_host_list/")){
        document.getElementById('ifrID').src=IframeUrl + "search?" + data;
    }else{
        document.getElementById('ifrID').src=IframeUrl + "&" + data;
    }
}
AddHost();
EditHost();