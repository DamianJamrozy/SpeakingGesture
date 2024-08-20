<!-- Translator.php -->
<?php include 'components/header-component-app.php'; ?>
<?php include 'components/menu-component-app.php'; ?>

<div class="content">
    <div class="container">
        <div class="hero">
            <h1>Tłumacz</h1>

            <div class="app-box">
                <div class="app-camera" id="camera-view">
                    <div class="info-required">
                        <center><h3> UWAGA! </h3></center>
                    
                        <p>Aplikacja do poprawnego działania wykorzystuje kamerę internetową.</p>
                        <p>Upewnij się, że jest ona podłączona do urządzenia przed jej udostępnieniem.<br><br></p>
                        
                         <div style="text-align:center; padding-top:2vh; padding-bottom:5vh;">
                            <span class="button-v1" id="camera-access">Udostępnij obraz z kamery</span>
                        </div>
                        <p> *Informujemy, że system przetwarza obraz z kamery w czasie rzeczywistym, jednakże nie dokonuje on jego zapisu ani przechowywania. </p>
                    </div>
                </div>
                <div class="sign-preview">
                    <div class="info-required">
                        <center><h3> Informacja </h3></center>
                        <p>Okno to odpowiada za wizualizację gestu.</p>
                        <p>Wybierz gest za pomocą paska wyszukiwania lub pokaż go z wykorzystaniem kamery internetowej aby odtworzyć jego wizualizację.</p>
                        <b style="color:red;">Tutaj ma się wczytać gest:<br>
                            a) wpisany przez użytkownika<br>
                            b) Wykryty przez program - przy czym powinien wykryć go przynajmniej 3-5 razy pod rząd aby go załadować<br></b>
                    </div>
                </div>
            </div>

            <div class="app-text-box">
                <div class="app-microphone" id="microphone">
                </div>
                <div class="app-text">
                    <input type="text" placeholder="Wpisz szukany gest..." id="sign-text">
                </div>
                <div class="text-send" id="send-text">
                    
                </div>
            </div>
    </div>
</div>

<script type="text/javascript" src="../../scripts/js/translator.js"></script>
<?php include 'components/footer-component-app.php'; ?>