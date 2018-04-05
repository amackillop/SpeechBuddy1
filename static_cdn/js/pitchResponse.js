function precisionRound(number, precision) {
	var factor = Math.pow(10, precision);
	return Math.round(number * factor) / factor;
  }
  
  function linspace (a, b, n) {
	if (typeof n === 'undefined') n = Math.max(Math.round(b - a) + 1, 1)
	if (n < 2) {
	  return n === 1 ? [a] : []
	}
	var i,ret = Array(n)
	n--
	for (i = n;i >= 0;i--) {
	  ret[i] = precisionRound((i * b + (n - i) * a) / n, 2)
	}
	return ret
  }
  
  
  
  function PitchTabCreate(data){
	  var ctx = document.getElementById("PitchLineChart");
	  var config = {
	type: 'line',
	data: {
	  labels: linspace(0,data.EndTime,data.V.length),
	  datasets: [{
		  data: data.V,
		  label: "Pitch:",
		  borderColor: "#3e95cd",
		  fill: false
		}
	  ]
	},
	options: {
	  title: {
		display: true,
		text: 'Pitch Analysis (s)'
	  },
	  legend: {
		  display: false
	  }
	}
  }
	  var myChart = new Chart(ctx, config );
  
  }

// function pitchResponse(data) {

// 	/*     pitch = document.getElementById("transcript"); */
// 	console.log("Pitch ran");
// 	/*     transcript.style.display = "block"; */

// 	$(document).ready(function () {
// 		google.charts.load('current', { packages: ['corechart', 'line'] });
// 		google.charts.setOnLoadCallback(drawBackgroundColor);

// 		function drawBackgroundColor() {
// 			var chartData = new google.visualization.DataTable();
// 			chartData.addColumn('number', 'X');
// 			chartData.addColumn('number', 'f0');
// 			chartData.addColumn('number', 'f1');

// 			chartData.addRows(data.pitch);
// 			var options = {
				
// 				width: 720,
// 				height: 350,
// 				'title': 'Fundemental Frequency',
// 				curveType: 'function',
// 				series: {
// 					0: { targetAxisIndex: 0 },
// 					1: { targetAxisIndex: 1 }
// 				},
// 				vAxes: {
// 					// Adds titles to each axis.
// 					0: { title: 'f0' },
// 					1: { title: 'f1' }
// 				},
// 				//												vAxis: {
// 				//													0: {viewWindow: {
// 				//																min: 0,
// 				//																max: 100
// 				//															},
// 				//														},
// 				//													1: {viewWindow: {
// 				//																min: 500,
// 				//																max: 1000
// 				//																}
// 				//															}
// 				//														}
// 				//													}
// 			};


// 			var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
// 			chart.draw(chartData, options);
// 		}
// 	})

// }