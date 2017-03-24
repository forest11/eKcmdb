/**
 * Created by pandonglin on 2017/1/15.
 */


(function (jq) {

    /*
    用于向后台发送请求的url
     */
    var requestUrl;

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

    /*
    初始化页面
    */
    function initPage() {
        bingClickFunction();
    }

    /*
    绑定页面标签点击事件
    */
    function bingClickFunction() {
        reloadPage();
        submitData();
        multiSelect();
    }

    
    /*
    重新加载页面
    */
    function reloadPage() {
        $(".reload_ths_page").on("click", function(){
            window.location.reload();
        })
    }

    /*
    提交对象
    */
    function submitData() {

        $("#submit_button").on("click", function(){
            $('.msg-error').remove();

            var data = {};
            var objId = $('.form-horizontal').attr('id');

            $("form input:text").each(function(){
                data[$(this).attr('name')]=$(this).val().trim();
            });

            $("form select").each(function(){
                data[$(this).attr('name')]=$(this).val();
            });

            $("form input:checkbox").each(function () {
                data[$(this).attr('name')]=$(this).is(':checked');
            });

            $("form textarea").each(function () {
                data[$(this).attr('name')]=$(this).val().trim();
            });

            var mulSelect = $('.right_select').attr('name');

            data[mulSelect] = [];
            $(".right_select option").each(function () {
                data[mulSelect].push($(this).val());
            });
            console.log(data);

            $.ajax({
                url: requestUrl + '?id=' + objId,
                type: 'POST',
                data: data,
                dataType: 'json',
                traditional: true,

                success: function(response){

                    if (response.status) {
                        var tag = '<div class="form-group"><div class="col-sm-4 col-sm-offset-6"><div class="msg-error">提交成功</div></div></div>';
                        $('.hr-line-dashed').after(tag);

                        setTimeout(function () {
                            $('.msg-error').remove();
                        }, 5000);
                    } else {
                        $.each(response.message, function (k, v) {
                            var tag = '<span class="msg-error">' + v[0].message + '</span>';
                            if (k == "__all__") {
                                $('.hr-line-dashed').append(tag)
                            } else if (k == 'msg-error'){
                                $('.hr-line-dashed').append(tag)
                            } else {
                                $("#" + k).parent().append(tag);
                            }
                        })
                    }
                }
            })
        })
    }


    /*
    多选框右移
    */
    function multiSelect() {

        /*
        多选框右移
        */
        $("#left_mv").on("click", function () {
            $('.left_select option:selected').each(function(){
                var tag = '<option value=' + $(this).val() + '>' + $(this).text() + '</option>';
                $(".right_select").append(tag);
                $(this).remove();
            });
        });

        /*
        多选框左移
        */
        $("#right-mv").on("click", function () {
            $('.right_select option:selected').each(function(){
                var tag = '<option value=' + $(this).val() + '>' + $(this).text() + '</option>';
                $(".left_select").append(tag);
                $(this).remove();
            });
        })
    }



    jq.extend({

        'initPage': function(url){
            requestUrl = url;
            initPage();
        }
    })
})(jQuery);