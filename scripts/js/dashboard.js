//Obs³uga podstawowa danych
let ilosc_gestow = 6;
let ilosc_nagran = 1100;
let czas_nagran = 0;

document.getElementById("ilosc_gestow").innerHTML = ilosc_gestow;
document.getElementById("ilosc_nagran").innerHTML = ilosc_nagran;

czas_nagran = (((ilosc_nagran * 4) / 60) / 60).toFixed(2);
document.getElementById("czas_nagran").innerHTML = czas_nagran + "h";

//Obs³uga wizualizacji
document.addEventListener('DOMContentLoaded', function () {
	const video = document.getElementById('dashboard-video');
	video.playbackRate = 0.5; // Ustawienie tempa odtwarzania na 0.5

	// Ukrycie kontrolek, po upewnieniu siê, ¿e wideo siê ³aduje
	video.oncanplay = function () {
		video.controls = false;
		video.style.opacity = "1"; // P³ynne wyœwietlanie wideo po jego za³adowaniu
	};
});



var chart = document.getElementById('chart').getContext('2d'),
    gradient = chart.createLinearGradient(0, 0, 0, 450);

gradient.addColorStop(0, 'rgba(0, 199, 214, 0.32)');
gradient.addColorStop(0.3, 'rgba(0, 199, 214, 0.1)');
gradient.addColorStop(1, 'rgba(0, 199, 214, 0)');

var options = {
	responsive: true,
	maintainAspectRatio: true,
	animation: {
		easing: 'easeInOutQuad',
		duration: 520
	},
	scales: {
		yAxes: [{
      ticks: {
        fontColor: '#5e6a81'
      },
			gridLines: {
				color: 'rgba(200, 200, 200, 0.08)',
				lineWidth: 1
			}
		}],
    xAxes:[{
      ticks: {
        fontColor: '#5e6a81'
      }
    }]
	},
	elements: {
		line: {
			tension: 0.4
		}
	},
	legend: {
		display: false
	},
	point: {
		backgroundColor: '#00c7d6'
	},
	tooltips: {
		titleFontFamily: 'Poppins',
		backgroundColor: 'rgba(0,0,0,0.4)',
		titleFontColor: 'white',
		caretSize: 5,
		cornerRadius: 2,
		xPadding: 10,
		yPadding: 10
	}
};

var chartInstance = new Chart(chart, {
    type: 'line',
    data: data,
		options: options
});

document.querySelector('.open-right-area').addEventListener('click', function () {
    document.querySelector('.app-right').classList.add('show');
});

document.querySelector('.close-right').addEventListener('click', function () {
    document.querySelector('.app-right').classList.remove('show');
});

document.querySelector('.menu-button').addEventListener('click', function () {
    document.querySelector('.app-left').classList.add('show');
});

document.querySelector('.close-menu').addEventListener('click', function () {
    document.querySelector('.app-left').classList.remove('show');
});