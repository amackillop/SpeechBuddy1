function EmotionPieCreate(data){
    wpmTranscript();
    var ctx = document.getElementById("EmotionTextPieChart");
    var config = {
    type: 'doughnut',
    data: {
      labels: ["Sadness", "Joy", "Anger", "Disgust", "Fear"],
      datasets: [
        {
          label: "Population (millions)",
          backgroundColor: ["#5dade2", "#FFC300 ","#C70039 ","#28b463 ","#af7ac5"],
          data: data.AvgT
        }
      ]
    },
    options: {
				responsive: true,
				legend: {
					position: 'top',
				},
				title: {
					display: true,
					text: 'Speech Emotional Context (Text)'
				},
			}
}
    var myChart = new Chart(ctx, config );


}