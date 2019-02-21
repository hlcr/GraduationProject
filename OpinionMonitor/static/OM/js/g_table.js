/**
 * Created by user on 2016/11/27 0027.
 */
$.getJSON('/OpinionMonitor/search/kwl/kwl.json',{num:15}).done(function (data) {
    console.log(data);
    var table1 = $('#data_table1');
    var table2 = $('#data_table2');
    var table3 = $('#data_table3');
    var i = 0;
    for (var word in data){
        table_html = '<tr><td>'+word +'<td>'+data[word]+'<tr>';
        if (i<5){
            table1.append(table_html)
        }else if(i<10){
            table2.append(table_html)
        }else{
            table3.append(table_html)
        }
        i += 1;


    }
}).fail(function () {

});


