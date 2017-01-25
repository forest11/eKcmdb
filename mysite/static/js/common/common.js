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


var ChangeBus = function (ths) {
    var BusId = $(ths).parent().parent().attr("id");
    var SerList = $("#"+BusId+" td:eq(1) span").text().trim().split(' ');
    $("#newinput").children().remove();
    $.each(SerList, function (k ,v) {
        var tag = '<input class="col-sm-5 col-sm-offset-4" type="text" name="service" value="'+v+'">' +
            '<a class="fa fa-minus-circle col-sm-2" style="margin-top: 4px;" onclick="DelTag(this);"></a>';
        $("#newinput").append(tag);
    });
    $(".row span[name='name']").text($("#"+BusId+" td:eq(0)").text());
    $(".row textarea[name='memo']").text($("#"+BusId+" td:eq(2)").text());
    $(".modal-body").attr("change_id", BusId);
    $(ths).attr("data-target","#myModal");
};

function Newinput(ths){
    var tag = '<input class="col-sm-5 col-sm-offset-4" type="text" name="service" placeholder="服务名+端口">' +
        '<a class="fa fa-minus-circle col-sm-2" style="margin-top: 4px;" onclick="DelTag(this);"></a>';
    $("#newinput").append(tag);
}

function DelTag(ths) {
    $(ths).prev().remove();
    $(ths).remove();
}

var BusinessSumbit = function () {
    $("#change_submit").on("click", function () {
        var BusId = $(".modal-body").attr("change_id");
        var service = "";
        $("#newinput input").each(function (k, v) {
            service = service + "-" + ($(this).val().trim());
        });
        var data = {};
        data = {
            "id": BusId,
            "name": $(".modal-body span[name='name']").text().trim(),
            "service": service,
            "memo": $("textarea[name='memo']").val()
        };
        console.log(data);

        $.ajax({
            url: '/common/business_list/',
            type: 'POST',
            data: data,
            dataType: 'json',
            success: function(data){
                $('.msg-error').remove();
                if(data.status){
                    $(".modal-body").append('<div id="msg-error" class="msg-error">修改成功</div>');
                    $("#"+BusId).find("td[name='memo']").text(data.summary.memo);
                    $("#"+BusId+" td:eq(1) span").remove();
                    $.each(data.summary.service, function (k ,v) {
                        var tag = '<span class="btn-xs btn-default">' + v + '</span>&nbsp';
                        $("#"+BusId+" td:eq(1)").append(tag);
                    });
                    $("#"+BusId).find("input[name='service']").text(data.summary.service);
                    console.log(data.summary.service)
                }else{
                    $.each(data.message, function (k, v) {
                        $(".modal-body").append('<div id="msg-error" class="msg-error">'+k+v[0].message+'</div>');
                    })
                }
            }
        })
    })
};


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
                $('#msg-error').val("操作失败")
            }
        }
    });
}

function ChangeSer(ths) {
    $(ths).attr("data-target","#myModal");
    console.log($(ths));
}


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
                $('#msg-error').val("操作失败")
            }
        }
    });
}

var UpdateSer = function () {
    $("#submit_service_update").on("click", function () {

    });
};


AddBusiness();
AddService();
BusinessSumbit();
UpdateSer();