function volumeResponse(data) {

	/*     pitch = document.getElementById("transcript"); */
	console.log("Volume ran");
	/*     transcript.style.display = "block"; */

	$(document).ready(function () {
		google.charts.load('current', { packages: ['corechart', 'line'] });
		google.charts.setOnLoadCallback(drawBackgroundColor);

		function drawBackgroundColor() {
			var chartData = new google.visualization.DataTable();
			chartData.addColumn('number', 'X');
			chartData.addColumn('number', 'Volume');
			chartData.addRows(data.volume);
			var options = {
				width: 720,
				height: 350,
				title: 'Volume',
				curveType: 'function',
				series: {
					0: { targetAxisIndex: 0 }
				},
				vAxes: {
					// Adds titles to each axis.
					0: { title: 'Volume' }
				}
			}

			var chart = new google.visualization.LineChart(document.getElementById('chart_div_volume'));
			chart.draw(chartData, options);
		}
	})

}

function resizeChart() {
	chart.draw(data, options);
}
if (document.addEventListener) {
	window.addEventListener('resize', resizeChart);
}
else if (document.attachEvent) {
	window.attachEvent('onresize', resizeChart);
}
else {
	window.resize = resizeChart;
}