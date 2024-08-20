<!-- menu.php -->
<body>

<?php
// Pobierz nazwę aktualnie uruchomionego pliku (np. index.php)
$current_page = basename($_SERVER['PHP_SELF']);
?>

<nav>
    <ul>
        <li> <a class="logo-bar" href="Index.php"><img class="logo-image" src="../img/icons/logo-white.svg">Speaking Gesture</a> </li>
        <li class="nav-right last"> <a href="app/Dashboard.php"> <span class="button-v1">Przejdź do aplikacji</span> </a></li>
        <li class="nav-right"><a href="#" id="login-off" class="login-off"><span class="button-v2">Zaloguj się</span></a></li>
        <li class="nav-right"> <a href="About.php" class="<?= $current_page == 'About.php' ? 'active' : '' ?>">O nas</a></li>
        <li class="nav-right"> <a href="Project.php" class="<?= $current_page == 'Project.php' ? 'active' : '' ?>">O projekcie</a> </li>
        <li class="nav-right"> <a href="Index.php" class="<?= $current_page == 'Index.php' ? 'active' : '' ?>">Home</a></li>
    </ul>
</nav>
