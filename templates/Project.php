<!-- Project.php -->
<?php include 'components/header-component.php'; ?>
<?php include 'components/menu-component.php'; ?>

<div class="content">
    <div class="container">
        <div class="hero">
            <span class="button-v1 transparent"> Speaking Gesture  </span>
            <h1>Informacje o projekcie</h1>
            <p class="h1-more">Projekt został stworzony jako część pracy dyplomowej opracowanej <br>
            przez inż. Damiana Jamrożego, studenta Uniwersytetu Rzeszowskiego.<br>
            Pod opieką promotora dr. inż. Bogusława Twaroga </p>
            
            <div class="teaser"></div>
        </div>
        <div>
            
            <div class="timeline"> </div>

            <div class="glow-circle">
                <h2>Opis projektu</h2>

                <p>Pełny opis zagadnienia można znaleźć klikając przycisk poniżej.</p>
                <br><br>
                 <a href="#"><span class="button-v1 transparent"> Otwórz pracę magisterską  </span></a>
            </div>

            <div class="boxes">
                <div class="box-half">
                    <img class="icons-box" src="../img/icons/icon1.svg">
                    <h3> Projekt - Praca magisterska </h3>
                    <p>Pomysł projektu zaproponowany przez dr inż. Wojciecha Kozioła spotkał się z aprobatą dwóch studentów inż. Patryka Arendta oraz inż. Damiana Jamrożego, którzy to podjęli się jego realizacji w ramach zbliżonej tematyki prac magisterskich. Dzieki wsparciu merytorycznemu dr inż. W. Kozioła oraz dr inż. Bogusława Twaroga udało im się stworzyć oprogramowanie, które łączy w sobie funkcje sztucznej inteligencji oraz problematyki języka migowego. Oprogramowanie, docelowo ma za zadanie rejestrować, analizować i tłumaczyć język migowy na język naturalny, jednakże w późniejszych fazach projektu, aplikacja została poszerzona o funkcje nauki języka migowego wraz z analizą poprawności wykonywanych sekwencji gestów przez użytkownika. To wszystko jest możliwe dzięki rozwojowi techologii i popularyzacji sztucznej inteligencji.
                    </p>
                    <p><br><a href="About.php"> Poznaj nasz zespół </a></p>
                </div>
                <div class="box-half">
                     <img class="icons-box" src="../img/icons/icon2.svg">
                    <h3> Problematyka </h3>
                    <p>Nasz projekt skupia się wokół osób z dysfunkcjami słuchowymi. Osoby te, z powodu braku popularyzacji języka migowego, stale napotykają się na bariery językowe, które wykluczają ich z życia społecznego. Stworzona aplikacja ma wspierać ich w łatwiejszej komunikacji ze światem zewnętrznym, a także ma popularyzować naukę jezyka migowego. Prosty i intuicyjny interfejs użytkownika, w połączeniu z zaawansowaną logiką uczenia maszynowego pozwala na odczytywanie gestów w czasie rzeczywistym z jednoczesnym wyznaczaniem precyzji wykonanych sekwencji ruchów na podstawie utworzonego wcześniej modelu. Dzięki innowatorskim rozwiązaniom użytkownik może uczyć się języka migowego znacznie szybciej niż przy użyciu konkurencyjnych aplikacji bez konieczności wychodzenia z domu lub płacenia za drogie kursy.
                    </p>
                    <p><br><a href="app/Dashboard.php"> Przejdź do aplikacji </a></p>
                </div>
            </div>
            <div class="hidden-box-half-left"></div><div class="hidden-box-half-right"></div>
             

            <div class="box">
                <div class="box-left">
                    <img class="icons-box" src="../img/icons/icon3.svg">
                    <h3> Technologie </h3>
                    <p> Program dotyczący analizowania nagrań oraz trenowania modelu SI został utworzony za pośrednictwem języka PYTHON. Warstwa wizualna opracowana została za pomocą HTML, CSS, JavaScript.
  
                    </p>
                    <p><br><a href=""> Wyświetl pracę dyplomową </a></p>
                </div>
                <div class="box-right">
                    <img src="../img/previews/code-preview.svg">
                </div>
                <div style="clear: both;"></div>
                
            </div>
            <div class="hidden-box"></div>
            
            <div class="glow-circle how-it-works-txt"><h2>Jak działa program?</h2></div>
            <div class="how-it-works"></div>


        </div>



</div>
<?php include 'components/footer-component.php'; ?>
