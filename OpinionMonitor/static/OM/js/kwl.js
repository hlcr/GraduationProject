/**
 * Created by user on 2016/11/26 0026.
 */



// $.getJSON('./kwl/kwl.json').done(function(data){
//     console.log(data);
//     var ul = $('.widget-sentence-content > ul');
//     var li = ul.find('li');
//     li.remove();
//     for (var word in data){
//
//         ul.append('<li><a href="#list/67/"title="word"draggable="false"> word ' +
//             '<span class="badge"> num </span></a></li>'
//             .replace(/word/g,word).replace(/num/g,data[word]))
//     }

$.getJSON('./kwl/kwl.json').done(function(data){
    var ul = $('.widget-sentence-content > ul');
    var li = ul.find('li');
    li.remove();
    for (var word in data){
        var t_data = {"word":word,"num":data[word]};
        var html = template('keywordli', t_data);
        ul.append(html);
    }


}).fail(function (data) {
    console.log("fail to log json");
    console.log(data);
});



$.getJSON('./fpl/fpl.json').done(function(data){
    console.log(data);
    var ul = $('.widget.widget_hot > ul');
    console.log(ul);
    var li = ul.find('li');
    console.log(li);
    li.remove();

    for (var pid in data){
        var t_data = {"title":data[pid][0],"date":data[pid][1],"c_read":data[pid][2],"url":data[pid][3]};
        var html = template('passage_li', t_data);
        ul.append(html);
    }


}).fail(function (data) {
    console.log("fail to log json");
    console.log(data);
});


