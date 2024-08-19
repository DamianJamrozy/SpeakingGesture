// Wczytanie obrazu z kamery po zgodzie
document.getElementById('camera-access').addEventListener('click', function () {
    document.querySelector('.app-camera').innerHTML = '<img src="http://localhost:5000/video_feed" alt="Video feed" class="app-camera">';
});


// Wczytanie nagrania do podlgądu
document.getElementById('send-text').addEventListener('click', function () {
    const signText = document.getElementById('sign-text').value.trim();
    if (signText) {
        fetch(`../../scripts/php/search_video.php?sign=${signText}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log(data.path); // Zalogowanie ścieżki do wideo
                if (data.path) {
                    const existingVideo = document.querySelector('.sign-preview video');
                    if (existingVideo) {
                        existingVideo.remove();
                    }

                    const videoElement = document.createElement('video');
                    videoElement.src = data.path;
                    videoElement.autoplay = true;
                    videoElement.loop = true;
                    videoElement.muted = true;
                    videoElement.controls = true;

                    // Obsługa błędów odtwarzania
                    videoElement.onerror = function () {
                        console.error("Błąd podczas odtwarzania wideo.");
                        alert("Nie udało się odtworzyć wideo. Sprawdź, czy format pliku jest obsługiwany przez przeglądarkę.");
                    };

                    document.querySelector('.sign-preview').innerHTML = '';
                    document.querySelector('.sign-preview').appendChild(videoElement);
                } else {
                    alert("Nie znaleziono nagrania dla podanego gestu.");
                }
            })
            .catch(error => {
                console.error("Błąd podczas wyszukiwania nagrania:", error);
                alert("Wystąpił problem podczas wyszukiwania nagrania.");
            });
    } else {
        alert("Proszę wpisać nazwę gestu.");
    }
});

