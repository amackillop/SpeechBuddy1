function pitchResponse(data) {
	
/*     pitch = document.getElementById("transcript"); */
	console.log("pitch ran-");
/*     transcript.style.display = "block"; */
	
	$( document ).ready(function() {
	  google.charts.load('current', {packages: ['corechart', 'line']});
	  google.charts.setOnLoadCallback(drawBackgroundColor);

		function drawBackgroundColor() {
			  var chartData = new google.visualization.DataTable();
			  chartData.addColumn('number', 'X');
				chartData.addColumn('number', 'f0');
				chartData.addColumn('number', 'f1');

			  chartData.addRows(data.pitch);
				var options = {'title':'Fundemental Frequency',
												curveType: 'function',
												series: {
													0: {targetAxisIndex: 0},
													1: {targetAxisIndex: 1}
												},
												vAxes: {
													// Adds titles to each axis.
													0: {title: 'f0'},
													1: {title: 'f1'}
												}
											};
				

			  var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
			  chart.draw(chartData, options);
			}
	})

}