// Wczytanie nagrania do podlg¹du
document.getElementById('send-text').addEventListener('click', function () {
    const signText = document.getElementById('sign-text').value.trim();
    if (signText) {
        // Wywo³anie PHP, aby znaleŸæ œcie¿kê do wideo
        fetch(`../php/search_video.php?sign=${signText}`)
            .then(response => response.json())
            .then(data => {
                if (data.path) {
                    // Jeœli œcie¿ka zosta³a znaleziona, tworzymy element video
                    const existingVideo = document.querySelector('.sign-preview video');
                    if (existingVideo) {
                        existingVideo.remove();
                    }

                    const videoElement = document.createElement('video');
                    videoElement.src = data.path;
                    videoElement.autoplay = true;
                    videoElement.loop = true;
                    videoElement.muted = true; // Bez dŸwiêku
                    videoElement.controls = true; // Dodajemy kontrolki odtwarzania (opcjonalnie)

                    document.querySelector('.sign-preview').innerHTML = '';
                    document.querySelector('.sign-preview').appendChild(videoElement);
                } else {
                    alert("Nie znaleziono nagrania dla podanego gestu.");
                }
            })
            .catch(error => {
                console.error("B³¹d podczas wyszukiwania nagrania:", error);
                alert("Wyst¹pi³ problem podczas wyszukiwania nagrania.");
            });
    } else {
        alert("Proszê wpisaæ nazwê gestu.");
    }
});