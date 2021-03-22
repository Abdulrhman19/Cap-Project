var ChartJS = document.createElement('script');  
ChartJS.setAttribute('src','https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.4/Chart.min.js');
document.head.appendChild(ChartJS);

var ctx = document.getElementById('heart-chart');
var myChart = new ChartJS(ctx, {
    type: 'line',
    data: {
        labels: ['00:00', '06:00', '12:00', '18:00', '24:00'],
        datasets: [{
            label: '# of Votes',
            data: [50, 100, 10, 200],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});