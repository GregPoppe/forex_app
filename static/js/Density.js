
var IndexedData;

d3.json('/indexed_change').then(function(data4) {
  IndexedData = data4;
  IndexedData.forEach(trace => {
    trace.type='scatter';
    trace.marker={"color": "lightgrey", size:12}
  });

  IndexedData[IndexedData.length -1].marker = {"color": "red", size: 3};

  var layout = {
    showlegend: false,
    hovermode: false,


    shapes: [
      {
        line: {
          color: "black",
          size: 4,
          dash: 'dot'
        },
        type: "line",
        x0: 0,
        x1: 23,
        y0: 0,
        y1: 0
      }],




    margin: {
     t: 0,
     pad: 4
   },
   xaxis: {
    title: {
      text: 'Time (5 Minute Intervals)',
      font: {
        family: 'Courier New, monospace',
        size: 18,
        color: 'black'
      }
    },
  },

  yaxis: {
    title: {
      text: 'Change in Pips',
      font: {
        family: 'Courier New, monospace',
        size: 18,
        color: 'black'
      }
    },
  }



  };

  Plotly.newPlot('indexedChange', IndexedData, layout, {displayModeBar: false});
  });
