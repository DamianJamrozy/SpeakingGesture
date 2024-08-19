// Wczytanie obrazu z kamery po zgodzie
document.getElementById('camera-access').addEventListener('click', function () {
    document.querySelector('.app-camera').innerHTML = '<img src="http://localhost:5000/video_feed" alt="Video feed" class="app-camera">';
});


// Wczytanie nagrania do podlgądu
function playSignVideo() {
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
                if (data.path) {
                    const signPreview = document.querySelector('.sign-preview');
                    const existingVideo = signPreview.querySelector('video');
                    const infoRequired = signPreview.querySelector('.info-required');

                    // Usuwamy informację, jeśli istnieje
                    if (infoRequired) {
                        infoRequired.remove();
                    }

                    // Funkcja do dodania nowego wideo
                    function addNewVideo() {
                        const videoElement = document.createElement('video');
                        videoElement.src = data.path;
                        videoElement.autoplay = true;
                        videoElement.loop = true;
                        videoElement.muted = true;
                        videoElement.style.width = '100%';
                        videoElement.style.height = '100%';
                        videoElement.style.objectFit = 'cover';

                        // Dodanie ikony pauzy/odtwarzania
                        const playPauseOverlay = document.createElement('div');
                        playPauseOverlay.style.position = 'absolute';
                        playPauseOverlay.style.top = '50%';
                        playPauseOverlay.style.left = '50%';
                        playPauseOverlay.style.transform = 'translate(-50%, -50%)';
                        playPauseOverlay.style.fontSize = '5rem';
                        playPauseOverlay.style.color = 'white';
                        playPauseOverlay.style.display = 'none'; // Ukryte domyślnie
                        playPauseOverlay.style.pointerEvents = 'none'; // Aby nie przeszkadzało w klikaniu
                        playPauseOverlay.innerHTML = `
                            <svg viewBox="0 0 24 24" width="100" height="100" fill="white" class="play-icon">
                                <polygon points="9.33 7.5 16.5 12 9.33 16.5"></polygon>
                            </svg>
                            <svg viewBox="0 0 24 24" width="100" height="100" fill="white" class="pause-icon" style="display:none;">
                                <rect x="6" y="4" width="4" height="16"></rect>
                                <rect x="14" y="4" width="4" height="16"></rect>
                            </svg>
                        `;

                        signPreview.appendChild(playPauseOverlay);

                        // Dodanie funkcji do zatrzymywania/wznawiania odtwarzania po kliknięciu
                        videoElement.addEventListener('click', function () {
                            if (videoElement.paused) {
                                videoElement.play();
                                playPauseOverlay.querySelector('.play-icon').style.display = 'none';
                                playPauseOverlay.querySelector('.pause-icon').style.display = 'none';
                            } else {
                                videoElement.pause();
                                playPauseOverlay.querySelector('.pause-icon').style.display = 'block';
                                playPauseOverlay.querySelector('.play-icon').style.display = 'none';
                                playPauseOverlay.style.display = 'block';
                                setTimeout(() => {
                                    playPauseOverlay.style.display = 'none';
                                }, 500); // Ukrycie ikony pauzy po krótkim czasie
                            }
                        });

                        // Dodanie przycisku pełnego ekranu
                        const fullscreenButton = document.createElement('div');
                        fullscreenButton.style.position = 'absolute';
                        fullscreenButton.style.bottom = '10px';
                        fullscreenButton.style.right = '10px';
                        fullscreenButton.style.width = '30px';
                        fullscreenButton.style.height = '30px';
                        fullscreenButton.style.cursor = 'pointer';
                        fullscreenButton.style.zIndex = '10'; // Zawsze na wierzchu
                        fullscreenButton.innerHTML = `
                            <svg viewBox="0 0 24 24" width="30" height="30" fill="white">
                                <path d="M21 11V3h-8l3.29 3.29L7.41 15.17l1.42 1.42L18.71 7.71 22 11zM3 13v8h8l-3.29-3.29 10.88-10.88-1.42-1.42L7 16.29 3 13z"/>
                            </svg>
                        `;
                        signPreview.appendChild(fullscreenButton);

                        // Funkcja do przechodzenia w tryb pełnoekranowy
                        fullscreenButton.addEventListener('click', function () {
                            if (videoElement.requestFullscreen) {
                                videoElement.requestFullscreen();
                            } else if (videoElement.mozRequestFullScreen) { // Firefox
                                videoElement.mozRequestFullScreen();
                            } else if (videoElement.webkitRequestFullscreen) { // Chrome, Safari and Opera
                                videoElement.webkitRequestFullscreen();
                            } else if (videoElement.msRequestFullscreen) { // IE/Edge
                                videoElement.msRequestFullscreen();
                            }
                        });

                        // Ukrycie kontrolerów w trybie pełnoekranowym
                        videoElement.addEventListener('fullscreenchange', function () {
                            if (document.fullscreenElement) {
                                videoElement.controls = false; // Wyłączenie kontrolerów w pełnym ekranie
                            } else {
                                videoElement.controls = false; // Upewnienie się, że kontrolki są wyłączone po wyjściu z pełnego ekranu
                            }
                        });

                        // Dodaj wideo do kontenera
                        signPreview.appendChild(videoElement);
                    }

                    if (existingVideo) {
                        // Dodaj efekt fade-out do istniejącego wideo
                        existingVideo.classList.add('fade-out');

                        // Po krótkim opóźnieniu usuwamy stare wideo i dodajemy nowe
                        setTimeout(() => {
                            existingVideo.remove();
                            addNewVideo();
                        }, 500); // Opóźnienie 500ms, dostosuj w razie potrzeby
                    } else {
                        // Jeśli nie ma wideo, po prostu dodaj nowe wideo
                        addNewVideo();
                    }
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
}

// Obsługa kliknięcia na element z id "send-text"
document.getElementById('send-text').addEventListener('click', playSignVideo);

// Obsługa naciśnięcia klawisza Enter w polu tekstowym
document.getElementById('sign-text').addEventListener('keydown', function (event) {
    if (event.key === 'Enter') {
        playSignVideo();
    }
});
