<!-- Edu-progress.php -->
<?php include 'components/header-component-app.php'; ?>
<?php include 'components/menu-component-app.php'; ?>

<div class="content">
    <div class="container">
        <div class="hero">
            <h1>Nauka języka migowego</h1>

            <div class="app-box" style="margin-bottom:10vh;">
                <div class="results-gray-scale results-box"></div>
                <div class="results results-box">
                        <div class="results-ok">
                            <div class="results-ok-icon"></div>
                            <div class="results-text">
                                Gratulacje!<br>Gest został wykonany poprawnie!
                            </div>
                        </div>
                    <a href="">
                        <div class="results-return">
                            <div class="results-return-icon"></div>
                            <div class="results-text">
                                Wykonaj gest ponownie
                            </div>
                        </div>
                    </a>
                    <a href="Edu.php">
                        <div class="results-next">
                            <div class="results-next-icon"></div>
                            <div class="results-text">
                                Następny gest
                            </div>
                        </div>
                    </a>

                </div>
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
                        <center><h3 style="color:red;"> Błąd </h3></center>
                        <b><p style="color:red;">Gest nie został rozpoznany.</p>
                        <a href="Edu.php"><p style="color:red;">Kliknij TUTAJ aby wrócić do wyboru gestu.</p></a></b>
                    </div>
                </div>
            </div>

            <div class="app-text-box" style="display:none">
                <div class="app-text">
                    <input type="text" placeholder="Wpisz szukany gest..." id="sign-text">
                </div>
                <div class="text-send" id="send-text"></div>
            </div>
        </div>
    </div>

    <script type="text/javascript" src="../../scripts/js/edu.js"></script>
<?php include 'components/footer-component-app.php'; ?>
