
    chart = new NetChart({
         style: {
            node: { display: "text"},
            linkStyleFunction: linkStyle
        },
        
        filters:{
            nodeFilter:opFilter},
         
        data: { preloaded: 
                    {
                    "nodes":[
                        {"id":"qd39020","loaded":true,"style":{"label":"What is curiosity?","fillColor":"orange"}},
{"id":"qd68905","loaded":true,"style":{"label":"What is the time scale of curiosity?"}},
{"id":"a60280","loaded":true,"style":{"label":"seconds/within trial","fillColor":"white"}},
{"id":"a79023","loaded":true,"style":{"label":"minutes/within trial","fillColor":"white"}},
{"id":"a90009","loaded":true,"style":{"label":"lifelong/personality trait","fillColor":"white"}},
{"id":"qd75943","loaded":true,"style":{"label":"What is the structure of knowledges being seeken for?"}},
{"id":"a67943","loaded":true,"style":{"label":"few connections/busybody","fillColor":"white"}},
{"id":"a4582","loaded":true,"style":{"label":"closely connected/hunter","fillColor":"white"}},
{"id":"qd42158","loaded":true,"style":{"label":"What is the internal state computation that increases motivation?"}},
{"id":"a50961","loaded":true,"style":{"label":"learning progress","fillColor":"white"}},
{"id":"a45237","loaded":true,"style":{"label":"surprise","fillColor":"white"}},
{"id":"a56473","loaded":true,"style":{"label":"positive prediction error","fillColor":"white"}},
{"id":"ado2935","loaded":true,"style":{"label":"self-reported curiosity level","fillColor":"white"}},
{"id":"ado9435","loaded":true,"style":{"label":"willingness to stick to the current game","fillColor":"white"}},
{"id":"ado23948","loaded":true,"style":{"label":"KL divergence of belief state","fillColor":"white"}}

],
                    "links":[
                        {"id":"ld30565","from":"qd39020","to":"qd68905","type":"specification"},
{"id":"ld52809","from":"qd68905","to":"a60280","type":"answer"},
{"id":"ld13498","from":"qd68905","to":"a79023","type":"answer"},
{"id":"ld16370","from":"qd68905","to":"a90009","type":"answer"},
{"id":"ld88651","from":"qd39020","to":"qd75943","type":"specification"},
{"id":"ld3583","from":"qd75943","to":"a67943","type":"answer"},
{"id":"ld55037","from":"qd75943","to":"a4582","type":"answer"},
{"id":"ld65812","from":"qd39020","to":"qd42158","type":"specification"},
{"id":"ld72598","from":"qd42158","to":"a50961","type":"answer"},
{"id":"ld3121","from":"qd42158","to":"a45237","type":"answer"},
{"id":"ld31591","from":"qd42158","to":"a56473","type":"answer"},
{"id":"lod94291","from":"a60280","to":"ado2935","type":"operational_def"},
{"id":"lod58238","from":"a67943","to":"ado2935","type":"operational_def"},
{"id":"lod53927","from":"a79023","to":"ado9435","type":"operational_def"},
{"id":"lod53111","from":"a67943","to":"ado9435","type":"operational_def"},
{"id":"lod114","from":"a45237","to":"ado23948","type":"operational_def"}
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
function opFilter(nodeData){
    return  nodeData.id[2]!='o';
}
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
