function EmotionStackedBarCreate(data){
    var sentencesEnd = data.sentencesEnd;
    sentencesEnd[sentencesEnd.length-2] = sentencesEnd[sentencesEnd.length-1];
    sentencesEnd.splice(-1,sentencesEnd.length-1);
    console.log(sentencesEnd);
    var ctx = document.getElementById("EmotionTextBarChart");
    var barChartData = {
			labels: sentencesEnd,
			datasets: [{
				label: 'Sadness',
				backgroundColor: '#5dade2',
				data: data.SadnessT
			}, {
				label: 'Joy',
				backgroundColor: '#FFC300',
				data: data.JoyT
			}, {
				label: 'Anger',
				backgroundColor: '#C70039',
				data: data.AngerT
			},{
				label: 'Disgust',
				backgroundColor: '#28b463',
				data: data.DisgustT
			},{
				label: 'Fear',
				backgroundColor: '#af7ac5',
				data: data.FearT
			}]

		};
	config = {
				type: 'bar',
				data: barChartData,
				options: {
					title: {
						display: true,
						text: 'Emotional Context Over time'
					},
					tooltips: {
						mode: 'index',
						intersect: false,
						callbacks: {
                            index: function(tooltipItem) {
                                console.log(tooltipItem.yLabel);
                                console.log(tooltipItem.xLabel);
                                return  Number(tooltipItem.xLabel) + '\n' + ;
                            }
                        }
					},
					responsive: true,
					scales: {
						xAxes: [{
							stacked: true,
						}],
						yAxes: [{
							stacked: true
						}]
					}
				}
			}
    var myChart = new Chart(ctx, config );

}