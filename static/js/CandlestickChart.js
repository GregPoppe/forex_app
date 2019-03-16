var CS;
var MACD;
var RSIData;


d3.json('/latest').then(function(data) {
  CS = data;
  d3.json('/MACD').then(function(data2) {
    MACD = data2;
      d3.json('/RSI').then(function(data3) {
        RSIData = data3;
        drawGraphs();
      });
    });
 });

function drawGraphs() {
  dataProcess();
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

}

function dataProcess() {
 var x = CS.map(a => a.time);
 var close = CS.map(a => a.ask_c);
 var high = CS.map(a => a.ask_h);
 var low = CS.map(a => a.ask_l);
 var open = CS.map(a => a.ask_o);


var trace1 = {
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




 var data = [trace1];

 var layout = {
   dragmode: 'zoom',
   title : 'EUR/USD Price 5 Minute',
   plot_bgcolor : '#rgba(16, 14, 15, 0.9)',
   showlegend : false,
   showgrid : true,
   gridwidth : 100,
   xaxis: {
     fixedrange: true,
     rangeslider: {
      visible: false
     }
   },
   yaxis: {
      fixedrange: true
   }
 };

 Plotly.newPlot('plot1', data, layout, {displayModeBar: false});

};




function dataProcessMACD() {
 var x = MACD.map(a => a.time);
 var MA_12 = MACD.map(a => a.Mov_Avg12);
 var MA_26 = MACD.map(a => a.Mov_Avg26);



 var trace1 = {
   x: x,
   y: MA_12,
   mode: 'lines'
 };

 var trace2 = {
   x: x,
   y: MA_26,
   mode: 'lines'
 };

 var layout = {
   showlegend: false,
   margin: {
    t: 0,
    pad: 4
  }
 };
 var data = [trace1, trace2];

 Plotly.newPlot('plot2', data, layout, {displayModeBar: false});

};




function dataProcessRSI() {
 var x = RSIData.map(a => a.time);
 var RSI = RSIData.map(a => a.RSI);



 var trace1 = {
   x: x,
   y: RSI,
   mode: 'lines'
 };

var layout = {
   showlegend: false,
   margin: {
    t: 0,
    pad: 4
  }
 };


 var data = [trace1];

 Plotly.plot('plot3', data, layout, {displayModeBar: false});

};