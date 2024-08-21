<!-- Edu.php -->
<?php include 'components/header-component-app.php'; ?>
<?php include 'components/menu-component-app.php'; ?>

<div class="content">
    <div class="container">
        <div class="hero">
            <h1>Nauka języka migowego</h1>

            <div class="category-box">
                <div id="category-objects">
                    <?php
                    $categories = [
                        'Zwroty grzecznościowe' => 'category1',
                        'Podstawowe zwroty' => 'category2',
                    ];
                    $baseDir = '../../video/';

                    foreach ($categories as $label => $categoryClass) {
                        $imageClass = $categoryClass === 'category1' ? 'category-image1' : 'category-image2';
                        echo "<div class=\"category $categoryClass\">";
                        echo "<div class=\"category-icon $imageClass\"></div>";
                        echo "<div class=\"category-title\">$label</div>";
                        echo "</div>";
                    }
                    ?>
                </div>

                <?php
                foreach ($categories as $label => $categoryClass) {
                    $categoryDir = $baseDir . $label;
                    $imageClass = $categoryClass === 'category1' ? 'category-image1' : 'category-image2';
                    if (is_dir($categoryDir)) {
                        echo "<div class=\"items\" id=\"$categoryClass-items\">";
                        $subDirs = glob($categoryDir . '/*', GLOB_ONLYDIR);

                        foreach ($subDirs as $subDir) {
                            $signName = basename($subDir);
                            echo "<div class=\"category $categoryClass\">";
                            echo "<div class=\"category-icon $imageClass\"></div>";
                            echo "<div class=\"category-title\" onclick=\"loadSign('$signName')\">$signName</div>";
                            echo "</div>";
                        }

                        echo "</div>";
                    }
                }
                ?>
            </div>

            <span id="back-to-category" class="button-v1 back-to-category">Powrót do kategorii</span>
        </div>
    </div>
</div>

<script type="text/javascript" src="../../scripts/js/category.js"></script>
<?php include 'components/footer-component-app.php'; ?>
