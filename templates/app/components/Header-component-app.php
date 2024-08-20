<!DOCTYPE html>
<html lang="pl">

<?php
// Pobierz nazwę aktualnie uruchomionego pliku (np. index.php)
$current_page = basename($_SERVER['PHP_SELF']);
?>

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/x-icon" href="../../img/icons/logo-white.svg">
    <title>Speaking Gesture - App</title>

    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="../../style/app.css" title="Domyślny styl" type="text/css">

    <?php if ($current_page == 'Dashboard.php'){ ?>
        <link rel="stylesheet" href="../../style/dashboard.css" title="Domyślny styl" type="text/css">
    <?php } ?>
    
</head>