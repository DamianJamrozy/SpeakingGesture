<?php
if (isset($_GET['sign'])) {
    $sign = $_GET['sign'];
    $baseDir = '../../video/';
    
    // Znajdujemy wszystkie podkatalogi w 'video/'
    $directories = glob($baseDir . '*', GLOB_ONLYDIR);

    $found = false;
    foreach ($directories as $dir) {
        // Znajdujemy podkatalogi w aktualnym katalogu
        $subDirs = glob($dir . '/*', GLOB_ONLYDIR);
        foreach ($subDirs as $subDir) {
            $videoPath = $subDir . '/' . $sign . '.mp4';
            error_log("Weryfikacja œcie¿ki: " . $videoPath); // Debugging line
            if (file_exists($videoPath)) {
                echo json_encode(['path' => $videoPath]);
                $found = true;
                break 2; // Zakoñcz pêtlê, gdy znajdziemy plik
            }
        }
    }

    if (!$found) {
        echo json_encode(['error' => 'Nie odnaleziono nagrania']);
    }
} else {
    echo json_encode(['error' => 'Brak okreœlonego gestu']);
}
?>
