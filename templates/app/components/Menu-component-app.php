<!-- menu.php -->
<body>

<?php
// Pobierz nazwę aktualnie uruchomionego pliku (np. index.php)
$current_page = basename($_SERVER['PHP_SELF']);
?>

<nav class="nav-top">
    <ul>
        <li> <a class="logo-bar" href="../index.php"><img class="logo-image" src="../../img/icons/logo-white.svg">Speaking Gesture</a> </li>
        <li class="nav-right last"> <a href="#" id="login-off" class="login-off"> <span class="button-v1">Wyloguj się</span> </a></li>
        <li class="nav-right"> <a href="../Index.php">Wróć do strony głównej </a></li>
    </ul>
</nav>

<nav class="nav-left">
    <div><a href="Dashboard.php"><div class="icons-box1"></div></a><div class="<?= $current_page == 'Dashboard.php' ? 'active1' : '' ?>"></div>
    <div><a href="Translator.php"><div class="icons-box2"></div></a><div class="<?= $current_page == 'Translator.php' ? 'active2' : '' ?>"></div>
    <div><a href="Edu.php"><div class="icons-box3"></div></a><div class="<?= $current_page == 'Edu.php' ? 'active3' : '' ?> <?= $current_page == 'Edu-progress.php' ? 'active3' : '' ?>"></div>
</nav>

