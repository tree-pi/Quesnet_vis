
    chart = new NetChart({
         style: {
            node: { display: "text"},
            linkStyleFunction: linkStyle
        },
        filters:{
            nodeFilter:qFilter},
         
        data: { preloaded: 
                    {
                    "nodes":[
                        {"id":"q1", "loaded":true, "style":{"label":"What is the effect of curiosity?"}},
                        {"id":"q1-2", "loaded":true, "style":{"label":"What is the effect of curious state?"}},
                        {"id":"q1-1", "loaded":true, "style":{"label":"What is the effect of having a curious personality?"}},
                        {"id":"q0","loaded":true, "style":{"label":"What is curiosity?"},"hasanswer":true},
                        {"id":"a0","loaded":true,"style":{"label":"Curiosity as a personality trait measured by questionaire."}}
                    ],
                    "links":[
                        {"id":"l1","from":"q1", "to":"q1-1", "type":"specification","style":{ "toDecoration":"arrow"}},
                        {"id":"l2","from":"q1", "to":"q1-2", "type":"specification","style":{ "toDecoration":"arrow"}},
                        {"id":"l0","from":"q0","to":"q1","type":"definition","style":{"direction":"U"}},//todo: all "definition" relations should be undirected
                        {"id":"l0_0","from":"q0","to":'a0',"type":"answer","style":{ "toDecoration":"arrow"}}
                    ]}
                },
        container: document.getElementById("demo"),
        area: { height: 650 }
    });

    
    function linkStyle(link) {
        link.length = 2;
        link.items = [
            {   // Default item places just as the regular label.
                text: link.data.type,
                padding:2,
                backgroundStyle: {
                    fillColor: "rgba(86,185,247,1)",
                    lineColor: "rgba(86,185,247,0.4)"
                },
                textStyle: {
                    fillColor: "white"
                }
            }];
};

function qFilter(nodeData){
    return  nodeData.id[0]=='q';
}

function qaFilter(nodeData,linkData){
        return  nodeData.id[0]=='a' || nodeData.hasanswer;
    };

//add a button filter
$("#demo").append('<button type="button" id="showans" style="width:100px;margin-top:-200px;margin-left:20px;float:left;text-align: center">Show Answers</button>');
$("#demo").append('<button type="button" id="hideans" style="width:100px;margin-top:-200px; margin-left:150px;float:left;text-align: center">Hide Answers</button>');
function useQfilter(){
    
    chart.replaceSettings({
        filters:{
            nodeFilter:qFilter}
    })
    chart.updateFilters();
};
function useQAfilter(){
    console.log("showans")
    chart.replaceSettings({
        filters:{
            nodeFilter:qaFilter}
    })
    chart.updateFilters();
};

$(document).ready(function(){
        $("#showans").click(function(){
            useQAfilter()});



        $("#hideans").click(function(){
            console.log("hideans");
            useQfilter()});


})
