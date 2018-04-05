function EmotionStackedBarCreate(data){
    var sentencesEnd = data.sentencesEnd;
    var numberWithCommas = function(x) {
        return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    };
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
//						mode: 'index',
//						intersect: false,
						callbacks: {
                            label: function(tooltipItem, data) {
                                console.log(tooltipItem.xLabel);
                                changeEmotions(tooltipItem.xLabel, global_data.sentencesEnd)
                                return data.datasets[tooltipItem.datasetIndex].label + ": " + precisionRound(tooltipItem.yLabel,3);

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

function changeEmotions(info, sentencesEnd){
     if (!$("#Audio-transcript").is(":visible")) {
        AudioTranscript();

     }
     for (i = 0; i < document.getElementById('Audio-transcript').childNodes.length; i++) {
            document.getElementById('Audio-transcript').childNodes[i].className = "basic_transcript";
     }
     var value = sentencesEnd.indexOf(Number(info));
     console.log(value, typeof(sentencesEnd[0]), typeof(info));
    document.getElementById('Audio-transcript').childNodes[value].className = "reading_transcript";
    if(value == sentencesEnd.length-1){
        document.getElementById('Audio-transcript').childNodes[value+1].className = "reading_transcript";
    }
}