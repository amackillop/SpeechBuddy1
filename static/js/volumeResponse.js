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



function VolumeTabCreate(data){
    var ctx = document.getElementById("VolumeLineChart");
    var config = {
  type: 'line',
  data: {
    labels: linspace(0,data.EndTime,data.V.length),
    datasets: [{
        data: data.V,
        label: "Volume:",
        borderColor: "#3e95cd",
        fill: false
      }
    ]
  },
  options: {
    title: {
      display: true,
      text: 'Volume Analysis (s)'
    },
    legend: {
        display: false
    }
  }
}
    var myChart = new Chart(ctx, config );

}