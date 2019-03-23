var d3data;


var curX = 'MACD_Value';
var curY = 'RSI_Value';

//var xSel = d3.select("select").property('value');
//console.log(xSel);

d3.json(`/strategy_tester`).then(data => {
 d3data = data;
 parseData();
 console.log(curX);
 console.log(data);
 withD3();
});


function parseData(){

 d3data.forEach(function(data) {
   data.MACD_Value = parseFloat(data.MACD_Value);
   data.RSI_Value = parseFloat(data.RSI_Value);
   data.Change_2Hours = parseFloat(data.Change_2Hours);
 });
}


function newchart() {
 curX = d3.select('#x').property('value');
 curY = d3.select('#y').property('value');
 console.log(curX, curY);
 withD3();
};








function withD3() {



 var svgArea = d3.select("#scatter").select("svg");

 if (!svgArea.empty()) {
   svgArea.remove();
 }

 var svgWidth = window.innerWidth*0.9;
 var svgHeight = window.innerHeight*0.9;

 var margin = {
   top: 50,
   bottom: 50,
   right: 50,
   left: 50
 };

 var height = svgHeight - margin.top - margin.bottom;
 var width = svgWidth - margin.left - margin.right;

 // Append SVG element
 var svg = d3
   .select("#scatter")
   .append("svg")
   .attr("height", svgHeight)
   .attr("width", svgWidth);

 // Append group element
 var chartGroup = svg.append("g")
   .attr("transform", `translate(${margin.left}, ${margin.top})`);



   // create scales
   var xScale = d3.scaleLinear()
     .domain(d3.extent(d3data, d => d[curX]))
     .range([0, width]);

   var yScale = d3.scaleLinear()
     .domain(d3.extent(d3data, d => d[curY]))
     .range([height, 0]);

   // create axes
   var xAxis = d3.axisBottom(xScale);
   var yAxis = d3.axisLeft(yScale);

   // append axes
   chartGroup.append("g")
     .attr("transform", `translate(0, ${height})`)
     .call(xAxis);

   chartGroup.append("g")
     .call(yAxis);


   // append circles
   var circlesGroup = chartGroup.selectAll("circle")
     .data(d3data)
     .enter()
     .append("circle")
     .attr("cx", d => xScale(d[curX]))
     .attr("cy", d => yScale(d[curY]))
     .attr("r", d => Math.abs(d.Change_2Hours/3))
     .attr("fill", d => {
       if (d.Change_2Hours > 10) return "green";
       else if (d.Change_2Hours > -10) return "yellow";
       else return "red";
     })
     .attr("stroke-width", "1")
     .attr("stroke", "grey");


   // Step 1: Initialize Tooltip
   var toolTip = d3.tip()

     .attr("class", "d3-tip")
     .offset([80, -60])
     .html(function(d) {
       return (`State: ${d.Change_2Hours}<br>${curX}: ${d[curX]} <br>${curY}//: ${d[curY]}`);
     });

   // Step 2: Create the tooltip in chartGroup.
   chartGroup.call(toolTip);

   // Step 3: Create "mouseover" event listener to display tooltip
   circlesGroup.on("mouseover", function(d) {
     toolTip.show(d, this);
   })
   // Step 4: Create "mouseout" event listener to hide tooltip
     .on("mouseout", function(d) {
       toolTip.hide(d);
     });

};

withD3();


d3.select(window).on("resize", makeResponsive);