function pitchResponse(data) {

	/*     pitch = document.getElementById("transcript"); */
	console.log("Pitch ran");
	/*     transcript.style.display = "block"; */

	$(document).ready(function () {
		google.charts.load('current', { packages: ['corechart', 'line'] });
		google.charts.setOnLoadCallback(drawBackgroundColor);

		function drawBackgroundColor() {
			var chartData = new google.visualization.DataTable();
			chartData.addColumn('number', 'X');
			chartData.addColumn('number', 'f0');
			chartData.addColumn('number', 'f1');

			chartData.addRows(data.pitch);
			var options = {
				
				width: 720,
				height: 350,
				'title': 'Fundemental Frequency',
				curveType: 'function',
				series: {
					0: { targetAxisIndex: 0 },
					1: { targetAxisIndex: 1 }
				},
				vAxes: {
					// Adds titles to each axis.
					0: { title: 'f0' },
					1: { title: 'f1' }
				},
				//												vAxis: {
				//													0: {viewWindow: {
				//																min: 0,
				//																max: 100
				//															},
				//														},
				//													1: {viewWindow: {
				//																min: 500,
				//																max: 1000
				//																}
				//															}
				//														}
				//													}
			};


			var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
			chart.draw(chartData, options);
		}
	})

}