/**
 * Created by pandonglin on 2017/3/8.
 */

(function (jq) {
    /*
    用于保存当前作用域内的"全局变量"
     */
    var GLOBAL_DICT = {};

    /*
    用于向后台发送请求的url
     */
    var requestUrl;

    // 为字符串创建format方法，用于字符串格式化
    String.prototype.format = function (args) {
        return this.replace(/\{(\w+)\}/g, function (s, i) {
            return args[i];
        });
    };

    /*
     页面初始化（获取数据，绑定事件）
     */
    function initialize(pageNum) {

        $.ajax({
            url: requestUrl,
            type: 'GET',
            traditional: true,
            data: {'pager': pageNum},
            dataType: 'JSON',
            success: function (response) {
                if (response.status) {
                    initGlobal(response.data.global_dict);
                    initTableHeader(response.data.table_config);
                    initTableBody(response.data.page_info.page_start, response.data.data_list, response.data.table_config);
                    initPager(response.data.page_info.page_str);
                    initSearchMenu(response.data.condition_config);
                } else {
                    alert(response.message);
                }
            },
            error: function () {
                alert("加载页面失败。。");
            }
        })

    }


    /*
    加载页面
    */
    function reloadPage(pageNum) {
        var condition = JSON.stringify(bingSearchCondition());
        $.ajax({
            url: requestUrl,
            type: 'GET',
            traditional: true,
            data: {
                'condition': condition,
                'pager': pageNum
            },
            dataType: 'JSON',
            success: function (response) {
                if (response.status) {
                    initTableBody(response.data.page_info.page_start, response.data.data_list, response.data.table_config);
                    initPager(response.data.page_info.page_str);
                } else {
                    alert(response.message);
                }
            },
            error: function () {
                alert("加载页面失败。。");
            }
        })

    }

    /*
     初始化全局变量
     */
    function initGlobal(globalDict) {
        $.each(globalDict, function (k, v) {
            GLOBAL_DICT[k] = v;
        })
    }


    /*
     初始化表格的头部
     */
    function initTableHeader(tbConfig) {
        var $header = $('#table_head');

        $header.find('th').remove();

        /*
        //创建“选择列”
        var ck = document.createElement('th');
        ck.innerText = '选择';
        $header.find('tr').append(ck);

        // 创建“序号列”
        var num = document.createElement('th');
        num.innerText = '序号';
        $header.find('tr').append(num);
        */

        $.each(tbConfig, function (k, item) {
            if (item.display) {
                var tag = document.createElement('th');
                tag.innerText = item.title;
                $header.find('tr').append(tag);
            }
        });
    }

        /*
     更新成功，显示更新信息
     */
    function SuccessHandleStatus(content) {
        $('#msg-error').text(content);
        setTimeout(function () {
            $('#msg-error').text('');
        }, 5000);
    }



    /*
    初始化表格
    */
    function initTableBody(startNum, list, tbConfig) {
        var $body = $('#table_body');
        $body.empty();

        $.each(list, function (k1, row) {
            // row 表示从数据库获取的每行字典信息 {'id':'1','name': 'root' ...}
            // tbConfig 包含了所有表格的配置

            var tr = document.createElement('tr');
            tr.setAttribute('id', row['id']);
            tr.setAttribute('num', startNum + k1 + 1);
            /*
            // 创建每一行的CheckBox
            var tagTd = document.createElement('td');
            var tagCheckBox = document.createElement('input');
            tagCheckBox.type = 'checkbox';
            tagCheckBox.value = row['id'];
            $(tagTd).append(tagCheckBox);
            $(tr).append(tagTd);
            // 创建每一行的CheckBox
            var tagNum = document.createElement('td');
            tagNum.innerHTML = startNum + k1 + 1;
            $(tr).append(tagNum);
            */

            $.each(tbConfig, function (_, config) {
                // config中是对每一列数据的展示方式
                if (config.display) {
                    var td = document.createElement('td');

                    // 创建td的内容
                    var kwargs = {};
                    $.each(config.text.kwargs, function (k, v) {
                        if (v.startsWith('@@@')) {
                            var m2mFiled = v.substring(3, v.length);
                            kwargs[k] = ManyToManyByGlobalList(m2mFiled, row[config.q], config.separated);
                        } else if (v.startsWith('@@')) {
                            var foreignKey = v.substring(2, v.length);
                            kwargs[k] = getNameByGlobalList(foreignKey, row[config.q]);
                        } else if (v.startsWith('@')) {
                            if (row[v.substring(1, v.length)]){
                                kwargs[k] = row[v.substring(1, v.length)]
                            } else {
                                kwargs[k] = ''
                            }
                        } else {
                            kwargs[k] = v;
                        }
                    });
                    td.innerHTML = config.text.content.format(kwargs);

                    // 创建td的属性
                    $.each(config.attr, function (k, v) {
                        if (v.startsWith('@')) {
                            td.setAttribute(k, row[v.substring(1, v.length)]);
                        } else {
                            td.setAttribute(k, v);
                        }
                    });
                    $(tr).append(td);
                }
            });
            $body.append(tr);
        })
    }

    /*
     根据ID从全局变量中获取其对应的内容
     */
        /*外键字段*/
    function getNameByGlobalList(foreignKey, itemId) {
        var result;
        $.each(GLOBAL_DICT[foreignKey], function (k, v) {
            if (v.id == itemId) {
                result = v.name;
                return false;
            }
        });
        return result;
    }
        /*多对多字段*/
    function ManyToManyByGlobalList(m2mFiled, itemIds, separated) {
        /*m2mFiled为要显示的字段，itemIds为显示的值的id，separated为分割符*/
        var result;
        if ($.isArray(itemIds)){   /*多对多时，值可能数组*/
            $.each(itemIds, function (i, itemId) {
                $.each(GLOBAL_DICT[m2mFiled], function (k, v) {
                    if (v.id == itemId) {
                        if (result) {
                            result = result + separated + v.name;
                        } else {
                            result = v.name;
                        }
                        return false;
                    }
                })
            })
        } else {   /*不是数组时，替换当前字段值的id在全局变量中对应的值*/
            $.each(GLOBAL_DICT[m2mFiled], function (k, v) {
                if (v.id == itemIds) {
                    result = v.name;
                    return false;
                }
            })
        }
        return result;
    }



    /*
     初始化分页内容
     */
    function initPager(pageStr) {
        var $pager = $('#pager');
        $pager.empty();
        $pager.append(pageStr);
    }


    /*
    初始化搜索菜单
    */
    function initSearchMenu(config) {
        var searchMenu = $('.search-bar');
        searchMenu.empty();
        $.each(config, function (k, searchConditions) {

            if (searchConditions.condition_type == 'input') {
                var inputTag = '<div class="col-sm-3"> <input type="text" class="form-control m-b" name="'
                    + searchConditions.name + '" placeholder="' + searchConditions.text +'"> </div>';

                searchMenu.append(inputTag);

            } else if (searchConditions.condition_type == 'select') {
                var optionTag = '<option value="">' + searchConditions.text +'</option>';

                $.each(GLOBAL_DICT[searchConditions.global_name],function (k, v) {
                    optionTag = optionTag + '<option value="'+ v.id + '">' + v.name +'</option>';
                });
                var selectTag = '<div class="col-sm-2"><select class="form-control m-b" name="' + searchConditions.name
                    + '">' + optionTag + '</select></div>';

                searchMenu.append(selectTag);
            }
        });
    }

    /*
    绑定搜索的提交按钮
    */
    function bindSubmitSearch() {
        $('#search_submit').on('click', function () {
            reloadPage(1);
        })
    }


    
    /*
    构造搜索条件
    */
    function bingSearchCondition() {
        var data = {};

        $(".search-bar").children().each(function () {
            var inputCondition = $(this).find('input');
            var name = inputCondition.attr('name') +  "__contains";

            if (inputCondition.val()) {  //把value构造成一个数组，提交到后端
                data[name] = inputCondition.val().trim().replace('，', ',').split(',');  //逗号，分隔，实现多个查询
            }

            var selectCondition = $(this).find('select');
            var selectName = selectCondition.attr('name');
            if (selectCondition.val()) {
                data[selectName] = selectCondition.val().trim();
            }
        });

        return data;
    }

    /*
    刷新当前页面
    */
    function refreshData() {
        var currentPage = $('#pager').find("li[class='active']").text();
        initialize(currentPage);
    }


    /*
    删除数据页面
    */
    function deleteData(id) {
        $.ajax({
            url: requestUrl,
            type: 'POST',
            data: {id_list: id},
            traditional: true,
            success: function (response) {
                if (response.status) {
                    SuccessHandleStatus(response.message);
                } else {
                    alert(response.message);
                }
                refreshData();
            },
            error: function () {
                alert('操作失败');
            }
        })
    }



    jq.extend({

        'initMenu': function (target) {
            $(target).addClass('active').siblings().removeClass('active');
        },

        'initHtmlData': function(url){
            requestUrl = url;
            initialize(1);
            bindSubmitSearch();
        },

        'toNextPage': function (page_num) {
            initialize(page_num);
        },

        'deleteData': function (id) {
            deleteData(id);
        }
    })
})(jQuery);


