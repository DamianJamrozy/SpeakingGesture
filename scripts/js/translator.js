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
        //alert("Proszę wpisać nazwę gestu.");
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




// Web Speech API setup
const microphone = document.getElementById('microphone');
const signTextInput = document.getElementById('sign-text');
let recognition;
let isListening = false;

if ('webkitSpeechRecognition' in window) {
    recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'pl-PL';

    recognition.onresult = function (event) {
        let interimTranscript = '';
        for (let i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
                signTextInput.value += event.results[i][0].transcript;
            } else {
                interimTranscript += event.results[i][0].transcript;
            }
        }
        signTextInput.value = interimTranscript;
    };

    recognition.onerror = function (event) {
        console.error('Speech recognition error', event.error);
    };

    recognition.onend = function () {
        if (isListening) {
            recognition.start(); // Restart if not manually stopped
        }
    };
}

microphone.addEventListener('click', function () {
    if (!isListening) {
        isListening = true;
        signTextInput.placeholder = 'Trwa nasłuchiwanie...';
        recognition.start();
        microphone.classList.add('listening');
    } else {
        isListening = false;
        signTextInput.placeholder = 'Wpisz szukany gest...';
        recognition.stop();
        microphone.classList.remove('listening');
    }
});