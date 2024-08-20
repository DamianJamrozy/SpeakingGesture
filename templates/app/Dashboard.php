<!-- Dashboard.php -->
<?php include 'components/header-component-app.php'; ?>
<?php include 'components/menu-component-app.php'; ?>

<div class="content">
    <div class="container">
        <div class="hero">
            <h1>Dashboard</h1>

            <div class="app-main">
                <div class="main-header-line"></div>
                <div class="chart-row three">
                    <div class="chart-container-wrapper">
                        <div class="chart-container">
                            <div class="chart-info-wrapper">
                                <h2>Gestów</h2>
                                <span id="ilosc_gestow"></span>
                            </div>
                            <div class="chart-svg">
                                <svg viewBox="0 0 36 36" class="circular-chart pink">
                                    <path class="circle-bg" d="M18 2.0845
                                        a 15.9155 15.9155 0 0 1 0 31.831
                                        a 15.9155 15.9155 0 0 1 0 -31.831"></path>
                                    <path class="circle" stroke-dasharray="30, 100" d="M18 2.0845
                                        a 15.9155 15.9155 0 0 1 0 31.831
                                        a 15.9155 15.9155 0 0 1 0 -31.831"></path>
                                    <text x="18" y="20.35" class="percentage">30%</text>
                                </svg>
                            </div>
                        </div>
                    </div>
                    <div class="chart-container-wrapper">
                        <div class="chart-container">
                            <div class="chart-info-wrapper">
                                <h2>Próbek</h2>
                                <span id="ilosc_nagran"></span>
                            </div>
                            <div class="chart-svg">
                                <svg viewBox="0 0 36 36" class="circular-chart blue">
                                    <path class="circle-bg" d="M18 2.0845
                                        a 15.9155 15.9155 0 0 1 0 31.831
                                        a 15.9155 15.9155 0 0 1 0 -31.831"></path>
                                    <path class="circle" stroke-dasharray="60, 100" d="M18 2.0845
                                        a 15.9155 15.9155 0 0 1 0 31.831
                                        a 15.9155 15.9155 0 0 1 0 -31.831"></path>
                                    <text x="18" y="20.35" class="percentage">60%</text>
                                </svg>
                            </div>
                        </div>
                    </div>
                    <div class="chart-container-wrapper">
                        <div class="chart-container">
                            <div class="chart-info-wrapper">
                                <h2>Czas nagrań</h2>
                                <span id="czas_nagran"></span>
                            </div>
                            <div class="chart-svg">
                                <svg viewBox="0 0 36 36" class="circular-chart orange">
                                    <path class="circle-bg" d="M18 2.0845
                                        a 15.9155 15.9155 0 0 1 0 31.831
                                        a 15.9155 15.9155 0 0 1 0 -31.831"></path>
                                    <path class="circle" stroke-dasharray="90, 100" d="M18 2.0845
                                        a 15.9155 15.9155 0 0 1 0 31.831
                                        a 15.9155 15.9155 0 0 1 0 -31.831"></path>
                                    <text x="18" y="20.35" class="percentage">90%</text>
                                </svg>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="chart-row two">
                    <div class="chart-container-wrapper big">
                        <div class="chart-container">
                            <div class="chart-container-header">
                                <h2>Nauka modelu</h2>
                                <span>Prezentowany gest - Dzięki</span>
                            </div>
                            <div class="chart-data-details">
                                <div class="dashboard-visualization">
                                    <video id="dashboard-video" autoplay loop muted playsinline controls style="width: 100%; border-radius:5px; object-fit: cover; opacity: 0; transition: opacity 1s ease-in;">
                                        <source src="../../img/animations/visualization.mp4" type="video/mp4">
                                        Przykro mi ale twoja przeglądarka nie obsługuje plików video.<br>
                                        Zalecana jest zmiana przeglądarki na inną.
                                    </video>
                                    <p></p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="chart-container-wrapper small">
                        <div class="chart-container">
                            <div class="chart-container-header">
                                <h2>Gesty</h2>
                                <span href="#">Największa ilość próbek</span>
                            </div>
                            <div class="acquisitions-bar">
                                <span class="bar-progress rejected" style="width:200%;"></span>
                                <span class="bar-progress on-hold" style="width:200%;"></span>
                                <span class="bar-progress shortlisted" style="width:200%;"></span>
                                <span class="bar-progress applications" style="width:100%;"></span>
                            </div>
                            <div class="progress-bar-info">
                                <span class="progress-color applications"></span>
                                <span class="progress-type">Dzięki</span>
                                <span class="progress-amount">200</span>
                            </div>
                            <div class="progress-bar-info">
                                <span class="progress-color shortlisted"></span>
                                <span class="progress-type">Dziękuję</span>
                                <span class="progress-amount">200</span>
                            </div>
                            <div class="progress-bar-info">
                                <span class="progress-color on-hold"></span>
                                <span class="progress-type">Prosić</span>
                                <span class="progress-amount">200</span>
                            </div>
                            <div class="progress-bar-info">
                                <span class="progress-color rejected"></span>
                                <span class="progress-type">Cześć</span>
                                <span class="progress-amount">100</span>
                            </div>
                        </div>
                        <div class="chart-container applicants">
                            <div class="chart-container-header">
                                <h2>Ostatnio dodane</h2>
                                <span>Ostatni miesiąc</span>
                            </div>
                            <div class="applicant-line">
                                <img src="../../img/person/djamrozy.png" alt="profile">
                                <div class="applicant-info">
                                    <span>Cześć</span>
                                    <p>Dodane przez <strong>D. Jamroży</strong></p>
                                </div>
                            </div>
                            <div class="applicant-line">
                                <img src="../../img/person/djamrozy2.jpg" alt="profile">
                                <div class="applicant-info">
                                    <span>Proszę</span>
                                    <p>Dodane przez <strong>D. Jamroży</strong></p>
                                </div>
                            </div>
                            <div class="applicant-line">
                                <img src="../../img/person/djamrozy.png" alt="profile">
                                <div class="applicant-info">
                                    <span>Prosić</span>
                                    <p>Dodane przez <strong>D. Jamroży</strong></p>
                                </div>
                            </div>
                            <div class="applicant-line">
                                <img src="../../img/person/djamrozy2.jpg" alt="profile">
                                <div class="applicant-info">
                                    <span>Dzięki</span>
                                    <p>Dodane przez <strong>D. Jamroży</strong></p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
<?php include 'components/footer-component-app.php'; ?>
