document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("ajax-newsletter-form");
    const input = document.getElementById("newsletter-email");
    const messageContainer = document.getElementById("newsletter-message");

    if (!form) return;

    form.addEventListener("submit", function (e) {
        e.preventDefault(); // Bloque le rechargement de la page

        const emailValue = input.value.trim();
        
        // Nettoyage visuel préalable des messages
        messageContainer.className = "mt-4 text-xs font-medium";
        messageContainer.classList.remove("hidden");
        messageContainer.textContent = "Inscription en cours...";
        messageContainer.style.color = "#a1a1aa"; // Couleur stone-400

        // Récupération du token CSRF requis par Django
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || "";

        // Envoi de la requête AJAX vers le serveur
        fetch("/users/newsletter/subscribe/", {  // Ajuste l'URL selon ton fichier urls.py
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({ email: emailValue })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                messageContainer.textContent = data.message;
                messageContainer.style.color = "#34d399"; // Vert émeraude succès
                form.reset(); // Vide le champ texte
                
                // Petit effet premium : on fait disparaître le formulaire après 3 secondes
                setTimeout(() => {
                    form.style.display = "none";
                }, 2000);

            } else if (data.status === "info") {
                messageContainer.textContent = data.message;
                messageContainer.style.color = "#fbbf24"; // Ambre info
                form.reset();
            } else {
                messageContainer.textContent = data.message;
                messageContainer.style.color = "#f87171"; // Rouge erreur
            }
        })
        .catch(error => {
            console.error("Erreur Newsletter:", error);
            messageContainer.textContent = "Une erreur technique est survenue. Veuillez réessayer.";
            messageContainer.style.color = "#f87171";
        });
    });
});