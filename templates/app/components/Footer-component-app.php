<footer>
    <div class="footer-bottom">
        <div class="footer-bottom-left copyright">© 2024 SpeakingGesture by <a href="https://github.com/DamianJamrozy" target="_blank">Damian Jamroży</a>. All Rights Reserved.</div>
        <div class="footer-bottom-right">
            <h3><img style="width:2em;" src="../../img/icons/logo-white.svg">Speaking Gesture</h3>
        </div>
    </div>
</footer>

<?php
// Pobierz nazwę aktualnie uruchomionego pliku (np. index.php)
    $current_page = basename($_SERVER['PHP_SELF']);

    if ($current_page == 'Dashboard.php'){ ?>
        <script type="text/javascript" src='../../scripts/js/dashboard.js'></script>
<?php } ?>

<script type="text/javascript" src='../../scripts/js/message.js'></script>
</body>
</html>