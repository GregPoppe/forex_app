
var MACD;


d3.json('/MACD').then(function(data) {
  MACD = data;
  dataProcessMACD();
  });


function dataProcessMACD() {
  var x = MACD.map(a => a.time);
  var MA_12 = MACD.map(a => a.Mov_Avg12);
  var MA_26 = MACD.map(a => a.Mov_Avg26);
  console.log(MA_12);



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
    showlegend: false
  };
  var data = [trace1, trace2];

  Plotly.newPlot('plot2', data, layout);
  
};