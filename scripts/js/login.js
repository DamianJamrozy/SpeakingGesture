// Pobierz wszystkie elementy z klasą "login-off"
var buttons = document.querySelectorAll(".login-off");

buttons.forEach(function (button) {
    button.addEventListener("click", function () {
        var messageDiv = document.getElementById("message");
        messageDiv.innerHTML = "Uwaga!<br>Trwa bezpłatny okres próbny aplikacji - logowanie nie jest wymagane";
        messageDiv.classList.add("show");

        // Ustawienie znikania po 10 sekundach
        setTimeout(function () {
            messageDiv.classList.remove("show");
        }, 10000); // 10000 ms = 10 sekund
    });
});