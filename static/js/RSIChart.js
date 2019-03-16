
var RSIData;


d3.json('/RSI').then(function(data) {
  RSIData = data;
  dataProcessRSI();
  });


function dataProcessRSI() {
  var x = RSIData.map(a => a.time);
  var RSI = RSIData.map(a => a.RSI);
  console.log(RSI);



  var trace1 = {
    x: x,
    y: RSI,
    mode: 'lines'
  };
  
  

  var data = [trace1];

  Plotly.plot('plot3', data);
  
};