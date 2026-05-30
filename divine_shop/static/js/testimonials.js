// --- GESTION DU CAROUSEL DES TÉMOIGNAGES (3 PAR LIGNE) ---
document.addEventListener("DOMContentLoaded", function () {
    const track = document.getElementById("testimonial-track");
    if (!track) return;

    const cards = document.querySelectorAll(".testimonial-card");
    const totalCards = cards.length;
    
    let currentIndex = 0;

    function getVisibleCardsCount() {
        if (window.innerWidth >= 1024) return 3; // Écran large
        if (window.innerWidth >= 640) return 2;  // Tablette
        return 1;                                // Mobile
    }

    function scrollTestimonials() {
        const visibleCards = getVisibleCardsCount();
        
        // Si on a moins ou pile le nombre de cartes visibles, pas besoin de scroller
        if (totalCards <= visibleCards) return;

        currentIndex++;

        // Si on a dépassé la fin, on réinitialise au début en douceur
        if (currentIndex > totalCards - visibleCards) {
            currentIndex = 0;
        }

        // Calcul de la largeur d'une carte + de son espace (gap)
        const cardWidth = cards[0].getBoundingClientRect().width;
        const gap = 32; // Équivalent à gap-8 de Tailwind (32px)
        
        // Calcul du déplacement en pixels
        const amountToMove = currentIndex * (cardWidth + gap);
        
        // Application de la translation CSS
        track.style.transform = `translateX(-${amountToMove}px)`;
    }

    // Défilement automatique toutes les 60 000 millisecondes (1 minute)
    const testimonialInterval = setInterval(scrollTestimonials, 60000);

    // Réajustement si l'utilisateur change la taille de son écran
    window.addEventListener("resize", function () {
        currentIndex = 0;
        track.style.transform = `translateX(0px)`;
    });
});