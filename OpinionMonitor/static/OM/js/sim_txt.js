/**
 * Created by user on 2016/11/27 0027.
 */
var button = $('.button.confirm');
var clear = $('.button.clear');
var txt_area = $('.s_text');
var csrf = $('#csrf_token input');
var csrf_token = csrf[0].getAttribute('value');
// console.log(button);

// 发送请求
button.on('click', function () {
    // 清空所有结果
    $(".result_text_area div").remove();

    $.ajaxSetup({
        data: {csrfmiddlewaretoken: csrf_token }
    });

    $.post('../sim_txt_result/',{'s_text':txt_area.val()}).done(function (data) {
        data = eval("("+data+")");
    console.log(data);
        generate_result(data)
}).fail(function (data) {
    console.log("fail to get json")
});
});

// 清空数据
clear.on('click',function () {
    txt_area.val("")
});

function generate_result(data) {

    var len = Object.getOwnPropertyNames(data).length;
    len = Math.ceil(Object.getOwnPropertyNames(data).length / 3);

    for (var i = 0; i < len; i++) {
        // 添加行
        $(".result_text_area").append('<div class="row" style="padding: 10px 0 10px 0" id="row' + i + '"></div>');
    }

    var j = 0;
    for (var pid in data) {
        var row_num = "row" + Math.floor(j / 3); //向下整除
        var t_data = {
            "content": data[pid][6],
            "c_read": data[pid][2],
            "c_reply": data[pid][3],
            "title": data[pid][0],
            "pDate": data[pid][1],
            "url": data[pid][4],
            "ratio": data[pid][5]
        };
        var html = template('result_passage', t_data);
        $(".result_text_area #" + row_num).append(html);
        j += 1;
    }
}


