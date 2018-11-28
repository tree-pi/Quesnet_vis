    chart = new NetChart({
        style: { node: { display: "text" } },
        container: document.getElementById("demo"),
        area: { height: 550 },
        data: { preloaded: 
                    {
                    "nodes":[
                        {"id":"n1", "loaded":true, "style":{"label":"Why would you stay up at night?"}},
                        {"id":"n2", "loaded":true, "style":{"label":"What is a good way to keep being awake?"}},
                        {"id":"n3", "loaded":true, "style":{"label":"What is a good way to keep being awake without annoying any others?"}}
                    ],
                    "links":[
                        {"id":"l1","from":"n1", "to":"n2", "style":{"fillColor":"red", "toDecoration":"arrow"}},
                        {"id":"l2","from":"n2", "to":"n3", "style":{"fillColor":"green", "toDecoration":"arrow"}},
                        {"id":"l3","from":"n3", "to":"n1", "style":{"fillColor":"blue", "toDecoration":"arrow"}}
                    ]}
                }
    });


    $("#btn").click(function() {
        chart.replaceSettings({
            data: { url: "https://zoomcharts.com/dvsl/data/net-chart/basic-example.json"
            }
        });
        chart.reloadData();
    });
