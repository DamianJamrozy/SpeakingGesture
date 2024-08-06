<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gesture Recognition</title>
    <style>
        #details {
            margin-top: 20px;
            display: none;
        }
        .gesture-detail {
            margin: 10px 0;
        }
        .gesture-detail span {
            display: inline-block;
            width: 200px;
        }
        .progress-container {
            position: relative;
            width: 100%;
        }
        .progress-container progress {
            width: 100%;
            height: 20px;
        }
        .progress-label {
            position: absolute;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
            font-weight: bold;
        }
    </style>
    <script>
        let intervalId;
        let previousData = [];

        async function fetchGestureDetails() {
            const response = await fetch('http://localhost:5000/gesture_details');
            const data = await response.json();
            const detailsDiv = document.getElementById('details');
            detailsDiv.innerHTML = '';

            data.forEach((item, index) => {
                const previousProbability = previousData[index] ? previousData[index].probability : 0;

                const detailDiv = document.createElement('div');
                detailDiv.className = 'gesture-detail';

                const label = document.createElement('span');
                label.textContent = `${item.gesture}: `;

                const progressContainer = document.createElement('div');
                progressContainer.className = 'progress-container';

                const progress = document.createElement('progress');
                progress.value = previousProbability;
                progress.max = 100;

                const progressLabel = document.createElement('div');
                progressLabel.className = 'progress-label';
                progressLabel.textContent = `${previousProbability.toFixed(2)}%`;

                progressContainer.appendChild(progress);
                progressContainer.appendChild(progressLabel);

                detailDiv.appendChild(label);
                detailDiv.appendChild(progressContainer);
                detailsDiv.appendChild(detailDiv);

                // Płynna aktualizacja wartości
                animateProgress(progress, previousProbability, item.probability, 1000);
                animateValue(progressLabel, previousProbability, item.probability, 1000);

                previousData[index] = item;
            });
        }

        function animateProgress(progress, start, end, duration) {
            const range = end - start;
            const startTime = performance.now();

            function updateProgress(currentTime) {
                const elapsedTime = currentTime - startTime;
                const value = start + (range * (elapsedTime / duration));
                progress.value = value;
                if (elapsedTime < duration) {
                    requestAnimationFrame(updateProgress);
                } else {
                    progress.value = end;
                }
            }

            requestAnimationFrame(updateProgress);
        }

        function animateValue(element, start, end, duration) {
            const range = end - start;
            const startTime = performance.now();

            function updateValue(currentTime) {
                const elapsedTime = currentTime - startTime;
                const value = start + (range * (elapsedTime / duration));
                element.textContent = `${value.toFixed(2)}%`;
                if (elapsedTime < duration) {
                    requestAnimationFrame(updateValue);
                } else {
                    element.textContent = `${end.toFixed(2)}%`;
                }
            }

            requestAnimationFrame(updateValue);
        }

        function toggleDetails() {
            const detailsDiv = document.getElementById('details');
            const button = document.getElementById('toggleButton');
            if (detailsDiv.style.display === 'none') {
                detailsDiv.style.display = 'block';
                button.textContent = 'Ukryj szczegóły';
                fetchGestureDetails();
                intervalId = setInterval(fetchGestureDetails, 1000);  // Aktualizuj co sekundę
            } else {
                detailsDiv.style.display = 'none';
                button.textContent = 'Pokaż szczegóły';
                clearInterval(intervalId);
            }
        }
    </script>
</head>
<body>
    <h1>Gesture Recognition</h1>
    <img src="http://localhost:5000/video_feed" alt="Video feed">
    <button id="toggleButton" onclick="toggleDetails()">Pokaż szczegóły</button>
    <div id="details"></div>
</body>
</html>
