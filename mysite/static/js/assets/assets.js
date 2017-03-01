/**
 * Created by Administrator on 2016/12/15.
 */
$(function() {
    $("#reset_host_add").on("click", function(){
        window.location.reload();
    });

    $("#submit_host_add").on("click", function(){
        var data = {};
        $("form input:text").each(function(){
            data[$(this).attr('name')]=$(this).val().trim();
        });
        $("form select").each(function(){
            data[$(this).attr('name')]=$(this).val().trim();
        });
        $("form input:checkbox").each(function () {
            data[$(this).attr('name')]=$(this).is(':checked');
        });
        $("form textarea").each(function () {
            data[$(this).attr('name')]=$(this).val().trim();
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
    $("#submit_host_edit").on("click", function(){
        var data = {};
        var host_id = $("form").attr("id");
        $("form input:text").each(function(){
            data[$(this).attr('name')]=$(this).val().trim();
        });
        $("form select").each(function(){
            data[$(this).attr('name')]=$(this).val().trim();
        });
        $("form input:checkbox").each(function () {
            data[$(this).attr('name')]=$(this).is(':checked');
        });
        $("form textarea").each(function () {
            data[$(this).attr('name')]=$(this).val().trim();
        });
        console.log(data);
        $.ajax({
            url: '/assets/host_edit/' + host_id +'/',
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

function change_info(ths) {
    var data = $(ths).attr("name") + "=" + $(ths).val().trim();
    var IframeUrl = $("#ifrID").attr("src");
    if(IframeUrl.endsWith("iframe_host_list/")){
        document.getElementById('ifrID').src=IframeUrl + "search?" + data;
    }else{
        document.getElementById('ifrID').src=IframeUrl + "&" + data;
    }
}

function search_host() {
    var data = "ip_or_hostname" + "=" + $("#search_input").val().trim();
    document.getElementById('ifrID').src="/assets/iframe_host_list/search?" + data;
}