// Pobierz wszystkie elementy z klasą "login-off"
let buttons = document.querySelectorAll(".login-off");

buttons.forEach(function (button) {
    button.addEventListener("click", function () {
        let messageDiv = document.getElementById("message");
        messageDiv.innerHTML = "Uwaga!<br>Trwa bezpłatny okres próbny aplikacji - logowanie nie jest wymagane";
        messageDiv.classList.add("show");

        // Ustawienie znikania po 10 sekundach
        setTimeout(function () {
            messageDiv.classList.remove("show");
        }, 10000); // 10000 ms = 10 sekund
    });
});



let buttons2 = document.querySelectorAll(".no-social-media-info");

buttons2.forEach(function (button2) {
    button2.addEventListener("click", function () {
        let messageDiv = document.getElementById("message");
        messageDiv.innerHTML = "Informacja!<br>Brak informacji odnośnie mediów społecznościowych wybranego użytkownika";
        messageDiv.classList.add("show");

        // Ustawienie znikania po 10 sekundach
        setTimeout(function () {
            messageDiv.classList.remove("show");
        }, 10000); // 10000 ms = 10 sekund
    });
});