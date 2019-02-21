// 基于准备好的dom，初始化echarts实例
var myChart = echarts.init(document.getElementById('main'));

/**
    拼接路径
 */
function appendPath(id,graph){ 
    var str = id;
    var links = graph.links;
    var i = 0;
    var map = {};
    for( i = 0 ; i < links.length; i++){
        map[links[i].target] = links[i].source;
    }
    while(true){           
        if(map[id] == undefined){
            break;
        }
        str = map[id]  +"->" + str;
        id = map[id] ;
    }
    return str;
}
        myChart.showLoading();
        $.get('../../static/OM/json/data.json').done(function (data) {
            var graph = eval("("+data+")");
            myChart.hideLoading();
            // 生成类别
            var categories = [];
            for (var i = 0; i < 20; i++) {
                categories[i] = {
                    name: '类目' + i
                };
            }


            graph.nodes.forEach(function (node) {
                node.itemStyle = null;//
                node.symbolSize = node.size *10;//强制指定节点的大小   
                // Use random x, y
                node.x = node.y = null;
                node.draggable = true;

            });

            option = {
                title: {
                    text: '热点词汇',
                    subtext: 'Default layout',
                    top: 'bottom',
                    left: 'right'
                },
                tooltip: {
                        formatter: function (params, ticket, callback) {//回调函数
                            var str = graph.nodes[params.dataIndex].id;
                            str = str + "--" +graph.nodes[params.dataIndex].value;
                         // document.getElementById("div1").innerHTML = str;
                         return str;//
         }

                },
                legend: [{
                    // selectedMode: 'single',
                    data: categories.map(function (a) {
                        return a.name;
                    })
                }],
                animationDuration: 1500,
                animationEasingUpdate: 'quinticInOut',  
                legend:{
                    show:false
                },  
                series : [
                    {
                        name: '热点词语',
                        type: 'graph',
                        layout: 'force',

                        force:{
                            // 支持设置成数组表达边长的范围，此时不同大小的值会线性映射到不同的长度。值越小则长度越长
                            edgeLength: [100, 300],
                            // 节点受到的向中心的引力因子。该值越大节点越往中心点靠拢。
                            gravity:0.05,
                            // 支持设置成数组表达斥力的范围，此时不同大小的值会线性映射到不同的斥力。值越大则斥力越大
                            repulsion: 100
                        },
                        data: graph.nodes,
                        links: graph.links,
                        categories: categories,
                        roam: true,
                        label: {
                            normal: {
                                show: true,
                                position: 'inside',
                                formatter: '{b}'
                            }
                        },
                        lineStyle: {
                            normal: {
                                color: 'source',
                                curveness: 0.3
                            }
                        }
                    }
                ]
            };

            myChart.setOption(option);
        });

        myChart.on('click', function (params) {
            // 打开对应页面
            console.log('../search/?keyword='+params.name);
            window.open('../search/?keyword='+params.name);
        });
