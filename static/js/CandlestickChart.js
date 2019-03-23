// plot buyRSI, SellRSI, buy MACD, sell MACD

var CS;
var MACD;
var RSIData;
var obsforDropdown;

var candleTrace;
var MACDTrace1;
var MACDTrace2;
var RSITrace;
var d3data;
var Ind;
var Dir;

var curX = 'MACD_Value';
var curY = 'RSI_Value';

//Ryan--------------------------------------------------------

function changeObs() {
  //console.log(this, this.__data__);
  var d_unix = d3.select('#timeSelect').property('value');

  d3.json(`/latest?ts=${d_unix}`).then(function(data) {
    CS = data;
    d3.json(`/latest_short?ts=${d_unix}`).then(function(data2) {
      CS_short = data2;
      d3.json(`/MACD?ts=${d_unix}`).then(function(data3) {
        MACD = data3;
        d3.json(`/MACD_short?ts=${d_unix}`).then(function(data4) {
          MACD_short = data4;
          d3.json(`/RSI?ts=${d_unix}`).then(function(data5) {
            RSIData = data5;
            d3.json(`/RSI_short?ts=${d_unix}`).then(function(data6) {
              RSIData_short = data6;
              drawGraphs();
            });
          });
        });
      });
    });
  });
}


function changeInd(value1) {
  
  d3.event.preventDefault();
  d3.select("#indselect-container").text(value1);
}

function changeInd2(value2) {

  d3.event.preventDefault();
  d3.select("#dirselect-container").text(value2);
}


ind_data = ["MACD","RSI", "Stochastics", "BollBand", "Williams R"];
ind_data2 = ["Buy", "Sell"];



// Example Code
function createIndSelect() {
  let container = d3.select('#indselect-container');
   container.html(`<select id="indselect">
     <option value="">Please Select One</option>
     <option value="MACD_Signal">MACD</option>
     <option value="RSI_Signal">RSI</option>  
     <option value="Stochastics_Signal">Stochastics</option>        
     <option value="BollBand_Signal">BollBand</option> 
     <option value="Williams_R_Signal">Williams R</option>
     </select>`);
   d3.select("#indselect").selectAll("a").data(ind_data).enter().append("a")
     .text(d=>d).classed("dropdown-item",true).on("click",changeInd);

}
createIndSelect();

function createDirSelect() {
  let container = d3.select('#dirselect-container');
 container.html(`<select id="dirselect" onchange="createTimeSelect()">
   <option value="">Please Select One</option>
   <option value="1">Buy</option>
   <option value="-1">Sell</option>
   </select>`);
 d3.select("#indselect2").selectAll("a").data(ind_data).enter().append("a")
   .text(d=>d).classed("dropdown-item",true).on("click",changeInd2);

}
createDirSelect();

function createTimeSelect() {
  let container = d3.select('#timeselect-container');
  Ind = d3.select('#indselect').property('value');
  Dir = d3.select('#dirselect').property('value');
 d3.json(`/observations?Ind=${Ind}&Dir=${Dir}`).then(function(data){
  //console.log(data);
  container.html("");
  var select = container.append('select').attr('id', 'timeSelect');
  select.selectAll('option').data(data).enter().append("option").attr('value', d => d.unix)
    .text(d=>moment.unix(d.unix).format("MMMM Do YYYY, h:mm a")).classed("dropdown-item",true);
  select.on("change",changeObs);
  changeObs();
});
}


//Albert---------------------------------------------------

function drawGraphs() {
  drawCandlestick();
  dataProcessMACD();
  dataProcessRSI();


var myPlot = document.getElementById('plot1');
myPlot.on('plotly_hover', function (eventdata){
    var points = eventdata.points[0],
        pointNum = points.pointNumber;

    Plotly.Fx.hover('plot2',[
        { curveNumber:0, pointNumber:pointNum },
        { curveNumber:1, pointNumber:pointNum }
    ]);

    Plotly.Fx.hover('plot3', [
        { curveNumber:0, pointNumber:pointNum }
    ]);
});

var myPlot2 = document.getElementById('plot2');
myPlot2.on('plotly_hover', function (eventdata){
    var points = eventdata.points[0],
        pointNum = points.pointNumber;

    Plotly.Fx.hover('plot1',[
        { curveNumber:0, pointNumber:pointNum }
    ]);

    Plotly.Fx.hover('plot3', [
        { curveNumber:0, pointNumber:pointNum }
    ]);
});

var myPlot = document.getElementById('plot3');
myPlot.on('plotly_hover', function (eventdata){
    var points = eventdata.points[0],
        pointNum = points.pointNumber;

    Plotly.Fx.hover('plot2',[
        { curveNumber:0, pointNumber:pointNum },
        { curveNumber:1, pointNumber:pointNum }
    ]);

    Plotly.Fx.hover('plot1', [
        { curveNumber:0, pointNumber:pointNum }
    ]);
});

}

function drawCandlestick() {
 
 var x = CS_short.map(a => a.time); // need to update /latest to have two different time variables
 //console.log(x);
 var close = CS_short.map(a => a.ask_c);
 var high = CS_short.map(a => a.ask_h);
 var low = CS_short.map(a => a.ask_l);
 var open = CS_short.map(a => a.ask_o);
 var low_full = CS.map(a => a.ask_l);
 var high_full = CS.map(a => a.ask_h);


candleTrace = {
   x: x,
   close: close,
   decreasing: {line: {color: 'red'}},
   high: high,
   increasing: {line: {color: 'green'}},
   line: {color: 'rgba(31,119,180,1)'},
   low: low,
   open: open,
   type: 'candlestick',
   xaxis: 'x',
   yaxis: 'y'
 };

 var data = [candleTrace];

 var layout = {
   dragmode: 'zoom',
   title : 'EUR/USD Price 5 Minute',
   plot_bgcolor : '#rgba(16, 14, 15, 0.9)',
   showlegend : false,
   showgrid : true,
   gridwidth : 100,
   xaxis: {
     showticklabels: false,
     fixedrange: true,
     rangeslider: {
      visible: false
     },
     range: [d3.min(x),
              new Date(d3.max(x)).getTime() + 15000000 + (new Date().getTimezoneOffset() * 60 * 1000)]
   },
   yaxis: {
      title: 'EUR/USD',
      fixedrange: true,
      range: [d3.min(low_full), d3.max(high_full)] // +-0.002
   }
 };

 Plotly.newPlot('plot1', data, layout, {displayModeBar: false}, {responsive: true});

};


function dataProcessMACD() {

 var x = MACD_short.map(a => a.time);
 var MA_12 = MACD_short.map(a => a.Mov_Avg12);
 var MA_26 = MACD_short.map(a => a.Mov_Avg26);

 var MA_12_full = MACD.map(a => a.Mov_Avg12);
 var MA_26_full = MACD.map(a => a.Mov_Avg26);
 var min;
 var max;


 MACDTrace1 = {
   x: x,
   y: MA_12,
   mode: 'lines',
   name: 'MA_12'
 };

 MACDTrace2 = {
   x: x,
   y: MA_26,
   mode: 'lines',
   name: 'MA_26'
 };

 if (d3.min(MA_12_full) < d3.min(MA_26_full)) {
  min = MA_12_full;
 } else {
  min = MA_26_full;
 }

 if (d3.max(MA_12_full) < d3.max(MA_26_full)) {
  max = MA_26_full;
 } else {
  max = MA_12_full;
 }

 var layout = {
   showlegend: false,
   margin: {
    t: 0,
    b: 2,
    pad: 4
   },


   xaxis: {

    showticklabels: false,
    range: [d3.min(x),
              new Date(d3.max(x)).getTime() + 15000000 + (new Date().getTimezoneOffset() * 60 * 1000)]
   },
   yaxis: {
      title: 'MACD',
      fixedrange: true,
      range: [d3.min(min), d3.max(max)] 
   }
 };
 var data = [MACDTrace1, MACDTrace2];

 Plotly.newPlot('plot2', data, layout, {displayModeBar: false}, {responsive: true});

};




function dataProcessRSI() {
 var x = RSIData_short.map(a => a.time);
 var RSI = RSIData_short.map(a => a.RSI);

 var RSI_full = RSIData.map(a => a.RSI);


 RSITrace = {
   x: x,
   y: RSI,
   mode: 'lines'
 };

var layout = {
   showlegend: false,
   margin: {
    t: 0,
    pad: 4
   },
   xaxis: {
    range: [d3.min(x),
              new Date(d3.max(x)).getTime() + 15000000 + (new Date().getTimezoneOffset() * 60 * 1000)]
   },
   yaxis: {
      title: 'RSI',
      fixedrange: true,
      range: [d3.min(RSI_full), d3.max(RSI_full)] 
   }
 };


 var data = [RSITrace];

 Plotly.newPlot('plot3', data, layout, {displayModeBar: false}, {responsive: true});

};

function adjustGraph() {
  candleTrace.x = CS.map(a => a.time); 
  candleTrace.close = CS.map(a => a.ask_c);
  candleTrace.high = CS.map(a => a.ask_h);
  candleTrace.low = CS.map(a => a.ask_l);
  candleTrace.open = CS.map(a => a.ask_o); 

  Plotly.redraw('plot1');

  MACDTrace1.x = MACD.map(a => a.time);
  MACDTrace1.y = MACD.map(a => a.Mov_Avg12);
  MACDTrace2.x = MACD.map(a => a.time);
  MACDTrace2.y = MACD.map(a => a.Mov_Avg26);

  Plotly.redraw('plot2');

  RSITrace.x = RSIData.map(a =>a.time);
  RSITrace.y = RSIData.map(a => a.RSI);

  Plotly.redraw('plot3');

}