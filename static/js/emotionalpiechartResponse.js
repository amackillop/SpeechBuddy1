function EmotionTabCreate(data){
    var ctx = document.getElementById("EmotionTextPieChart");
    var config = {
    type: 'doughnut',
    data: {
      labels: ["Sadness", "Joy", "Anger", "Disgust", "Fear"],
      datasets: [
        {
          label: "Population (millions)",
          backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
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
				animation: {
					animateScale: true,
					animateRotate: true
				}
			}
}
    var myChart = new Chart(ctx, config );

}