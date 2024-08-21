let urlParams = new URLSearchParams(window.location.search);
let sign = urlParams.get('sign');

document.addEventListener('DOMContentLoaded', function () {
    if (sign) {
        document.getElementById('sign-text').value = sign;
        document.getElementById('send-text').click();
    }
});

///////////////////////////// Wczytanie obrazu z kamery po zgodzie /////////////////////////////
let cameraOn = false;
function camera_start() {
    const cameraView = document.getElementById('camera-view');
    let imgElement = cameraView.querySelector('img');

    if (!imgElement) {
        // Jeśli obraz nie istnieje, twórz go
        document.getElementById("camera-view").innerHTML = "";
        imgElement = document.createElement('img');
        imgElement.classList.add('app-camera');
        cameraView.appendChild(imgElement);
    }

    imgElement.src = "http://localhost:5000/video_feed";
    imgElement.alt = "Video feed";

    cameraOn = true;
    // Wywołaj funkcję po raz pierwszy
    checkGestures();
}

document.getElementById('camera-access').addEventListener('click', camera_start);

///////////////////////////// Wczytanie nagrania do podglądu /////////////////////////////
function playSignVideo() {
    const signText = document.getElementById('sign-text').value.trim();
    if (signText) {
        fetch(`../../scripts/php/search_video.php?sign=${signText}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('#Error-T-1 Wykryto problem z działaniem sieci');
                }
                return response.json();
            })
            .then(data => {
                if (data.path) {
                    const signPreview = document.querySelector('.sign-preview');
                    const existingVideo = signPreview.querySelector('video');
                    const existingCaptionBar = signPreview.querySelector('.caption-bar');
                    const infoRequired = signPreview.querySelector('.info-required');

                    // Usuwamy informację, jeśli istnieje
                    if (infoRequired) {
                        infoRequired.remove();
                    }

                    // Czyszczenie inputa po odnalezieniu gestu
                    document.getElementById('sign-text').value = '';

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
                        videoElement.style.opacity = '0'; // Ukrycie wideo na początku
                        videoElement.style.transition = 'opacity 0.5s ease, filter 0.5s ease'; // Płynne przejście opacity i filtra (jasności)

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
                            <svg viewBox="0 0 24 24" width="100" height="100" fill="white" class="play-icon" style="display:none;">
                                <polygon points="9.33 7.5 16.5 12 9.33 16.5"></polygon>
                            </svg>
                            <svg viewBox="0 0 24 24" width="100" height="100" fill="white" class="pause-icon">
                                <rect x="6" y="4" width="4" height="16"></rect>
                                <rect x="14" y="4" width="4" height="16"></rect>
                            </svg>
                        `;

                        signPreview.appendChild(playPauseOverlay);

                        // Usuwanie starego paska z napisem, jeśli istnieje
                        if (existingCaptionBar) {
                            existingCaptionBar.remove();
                        }

                        // Dodanie paska z podpisem gestu
                        const captionBar = document.createElement('div');
                        captionBar.classList.add('caption-bar'); // Dodanie klasy dla łatwej identyfikacji
                        captionBar.style.position = 'absolute';
                        captionBar.style.bottom = '0';
                        captionBar.style.width = '100%';
                        captionBar.style.borderBottomRightRadius = '20px';
                        captionBar.style.backgroundColor = 'rgba(0, 0, 0, 0.5)'; // Czarny z 50% przezroczystością
                        captionBar.style.color = 'white';
                        captionBar.style.textAlign = 'center';
                        captionBar.style.padding = '10px';
                        captionBar.style.fontSize = '1.2rem';
                        captionBar.style.boxSizing = 'border-box'; // Upewnienie się, że padding nie wpłynie na szerokość
                        captionBar.style.opacity = '0'; // Ukrycie napisu na początku
                        captionBar.style.transition = 'opacity 0.5s ease'; // Płynne przejście opacity
                        captionBar.style.zIndex = '10'; // Ustawienie paska na wierzchu wideo
                        captionBar.innerText = signText; // Tekst z nazwy gestu

                        signPreview.appendChild(captionBar);

                        // Dodanie funkcji do zatrzymywania/wznawiania odtwarzania po kliknięciu
                        videoElement.addEventListener('click', function () {
                            if (videoElement.paused) {
                                videoElement.play();
                                playPauseOverlay.querySelector('.play-icon').style.display = 'none';
                                playPauseOverlay.querySelector('.pause-icon').style.display = 'none';
                                videoElement.style.filter = 'brightness(100%)'; // Płynne rozjaśnienie obrazu
                                captionBar.style.opacity = '1'; // Ponowne pokazanie paska przy wznowieniu
                                captionBar.style.zIndex = '10'; // Ustawienie paska na wierzchu po wznowieniu
                            } else {
                                videoElement.pause();
                                playPauseOverlay.querySelector('.pause-icon').style.display = 'block';
                                playPauseOverlay.querySelector('.play-icon').style.display = 'none';
                                playPauseOverlay.style.display = 'block';
                                videoElement.style.filter = 'brightness(50%)'; // Płynne przyciemnienie obrazu
                                captionBar.style.opacity = '0'; // Ukrycie paska podczas pauzy
                                setTimeout(() => {
                                    playPauseOverlay.style.display = 'none';
                                }, 500); // Ukrycie ikony pauzy po krótkim czasie
                            }
                        });

                        // Ukrycie kontrolerów w trybie pełnoekranowym (zablokowanie pełnego ekranu)
                        videoElement.addEventListener('fullscreenchange', function () {
                            if (document.fullscreenElement) {
                                document.exitFullscreen();
                            }
                        });

                        // Dodaj wideo do kontenera
                        signPreview.appendChild(videoElement);

                        // Płynne pojawienie się nowego wideo
                        setTimeout(() => {
                            videoElement.style.opacity = '1'; // Ustawienie pełnej widoczności

                            // Płynne pojawienie się paska z napisem po wideo
                            setTimeout(() => {
                                captionBar.style.opacity = '1'; // Ustawienie pełnej widoczności dla paska
                            }, 300); // Opóźnienie dla płynnego pojawienia się paska
                        }, 50); // Opóźnienie dla płynnego pojawienia się wideo
                    }

                    if (existingVideo) {
                        // Dodaj efekt fade-out do istniejącego wideo
                        if (existingCaptionBar) {
                            existingCaptionBar.style.opacity = '0'; // Ukrycie starego paska
                        }
                        existingVideo.style.opacity = '0';
                        existingVideo.style.transition = 'opacity 0.5s ease, filter 0.5s ease'; // Płynne przejście opacity i filtra (jasności)

                        // Po krótkim opóźnieniu usuwamy stare wideo i dodajemy nowe
                        setTimeout(() => {
                            if (existingCaptionBar) {
                                existingCaptionBar.remove();
                            }
                            existingVideo.remove();
                            addNewVideo();
                        }, 500); // Opóźnienie 500ms dla płynnego przejścia
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
        console.log("#O-T5 Wywołano funkcję bez podanego gestu.");
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


///////////////////////////// Obsługa kamery - detekcja gestów z importem z Pythona /////////////////////////////
let lastGesture = null;
let gestureCount = 0;
let isVisualizing = false;
let stopGestures = false; // Flaga do przerwania cyklicznego wywoływania

async function checkGestures() {
    if (stopGestures) {
        return; // Przerwij działanie funkcji, jeśli flaga jest ustawiona
    }

    try {
        const response = await fetch('http://localhost:5000/gesture_details');
        const data = await response.json();

        if (data.length > 0) {
            const detectedGesture = data[0].gesture;

            if (detectedGesture === lastGesture) {
                gestureCount++;
            } else {
                lastGesture = detectedGesture;
                gestureCount = 1;
            }

            if (gestureCount === 3) {
                console.log(`Gesture detected 3 times: ${detectedGesture}`);
                if (!isVisualizing) {
                    if (detectedGesture == sign) {
                        console.log("Gratulacje!");
                        document.querySelectorAll('.results-box').forEach(function (element) {
                            element.style.display = 'block';
                        });

                        if (cameraOn == true) {
                            // Zatrzymaj kamerę, gdy strona jest niewidoczna
                            fetch('http://localhost:5000/stop_camera')
                                .then(response => response.json())
                                .then(data => console.log(data.status))
                                .catch(error => console.error('Error stopping camera:', error));
                            document.querySelector('.app-camera').innerHTML = '<div style="margin:1vw; font-weight:600;">Kamera została wyłączona...</div>';
                            stopGestures = true; // Ustaw flagę, aby zatrzymać cykliczne wywoływanie checkGestures
                        }
                    }
                } else {
                    //Podoba Ci się kod? <3 Stworzenie tego programu w pełni zajęło mi dosłownie pół roku życia... Jak już masz kraść to oznacz mnie (np. mojego githuba) lub zacytuj moją pracę mgr. Prawnie - nie wyrażam zgody na wykorzystanie tego programu ani żadnych elementów z nim związanych w żaden sposób komercyjny / niekomercyjny. Zgoda może zostać udzielona indywidualnie - jeżeli chcesz złożyć prośbę napisz na maila damianjamrozy99@gmail.com ;)
                }
            }
        }
    } catch (error) {
        console.error('Error fetching gesture data:', error);
    } finally {
        if (!stopGestures) {
            // Dodaj opóźnienie przed ponownym wywołaniem tylko, jeśli nie zatrzymano funkcji
            setTimeout(checkGestures, 1000);  // 1 sekunda opóźnienia
        }
    }
}

function camera_stop() {
    if (cameraOn == true) {
        document.querySelector('.app-camera').innerHTML = '<div style="margin:1vw; font-weight:600;">Brak połączenia z kamerą.<br>Trwa nawiązywanie połączenia...</div>';
        stopGestures = true; // Ustaw flagę, aby zatrzymać cykliczne wywoływanie checkGestures
    }
}

///////////////////////////// Wyłączenie kamery po opuszczeniu zakładki /////////////////////////////
document.addEventListener('visibilitychange', function () {
    if (document.visibilityState === 'hidden') {
        if (cameraOn == true) {
            // Zatrzymaj kamerę, gdy strona jest niewidoczna
            fetch('http://localhost:5000/stop_camera')
                .then(response => response.json())
                .then(data => console.log(data.status))
                .catch(error => console.error('Error stopping camera:', error));
            camera_stop();
        }
    } else if (document.visibilityState === 'visible') {
        if (cameraOn == true) {
            // Uruchom kamerę, gdy strona staje się widoczna
            fetch('http://localhost:5000/start_camera')
                .then(response => response.json())
                .then(data => {
                    console.log(data.status);
                    camera_start();
                })

                .catch(error => console.error('Error starting camera:', error));
        }
    }
});
