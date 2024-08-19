<!-- index.php -->
<?php include 'components/header-component-app.php'; ?>
<?php include 'components/menu-component-app.php'; ?>

<div class="content">
    <div class="container">
        <div class="hero">
            <h1>Tłumacz</h1>

            <div class="app-box">
                <div class="app-camera">
                    zapytaj o wykorzystanie kamery / wczytaj po zgodzie
                    <img src="http://localhost:5000/video_feed" alt="Video feed" class="app-camera">
                </div>
                <div class="sign-preview">
                    Tutaj ma się wczytać gest:<br>
                        a) wpisany przez użytkownika<br>
                        b) Wykryty przez program - przy czym powinien wykryć go przynajmniej 3-5 razy pod rząd aby go załadować<br>
                </div>
            </div>

            <div class="app-text-box">
                <div class="app-microphone">

                </div>
                <div class="app-text">
                    <input type="text" placeholder="Wpisz szukany gest..." id="sign-text">
                </div>
                <div class="text-send">
                    
                </div>
            </div>
    </div>
       

</div>
<?php include 'components/footer-component-app.php'; ?>
