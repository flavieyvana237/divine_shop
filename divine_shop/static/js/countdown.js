document.addEventListener("DOMContentLoaded", function () {
    const countdownContainer = document.getElementById("promo-countdown");
    
    if (!countdownContainer) return; // Sécurité si pas de promo active sur la page

    // Extraction de la date depuis l'attribut HTML data-deadline
    const deadlineStr = countdownContainer.getAttribute("data-deadline");
    // Formatage compatible tous navigateurs (remplace les tirets par des slashs)
    const targetDate = new Date(deadlineStr.replace(/-/g, "/")).getTime();

    // Sélection des cases d'affichage
    const daysElement = document.getElementById("lbl-days");
    const hoursElement = document.getElementById("lbl-hours");
    const minutesElement = document.getElementById("lbl-minutes");
    const secondsElement = document.getElementById("lbl-seconds");

    function updateChrono() {
        const now = new Date().getTime();
        const difference = targetDate - now;

        if (difference <= 0) {
            clearInterval(chronoInterval);
            countdownContainer.innerHTML = "<p class='text-amber-500 italic font-serif text-sm py-2'>L'événement promotionnel a pris fin.</p>";
            return;
        }

        // Calculs des composants temporels
        const days = Math.floor(difference / (1000 * 60 * 60 * 24));
        const hours = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((difference % (1000 * 60)) / 1000);

        // Injection des valeurs avec formatage "00"
        daysElement.textContent = String(days).padStart(2, '0');
        hoursElement.textContent = String(hours).padStart(2, '0');
        minutesElement.textContent = String(minutes).padStart(2, '0');
        secondsElement.textContent = String(seconds).padStart(2, '0');
    }

    // Lancement immédiat puis toutes les secondes
    updateChrono();
    const chronoInterval = setInterval(updateChrono, 1000);
});