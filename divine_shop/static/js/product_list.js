document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('filter-form');
    const container = document.getElementById('products-container');
    const categoryInput = document.getElementById('category-input');
    const pageInput = document.getElementById('page-input');
    const searchInput = document.getElementById('search-input');
    const resetBtn = document.getElementById('reset-filters');

    // Fonction principale AJAX
    function fetchProducts(updateUrl = true) {
        // Opacité réduite pendant le chargement
        container.style.opacity = '0.5';

        const formData = new FormData(form);
        const params = new URLSearchParams();

        // On nettoie les valeurs vides pour garder une URL propre
        for (const [key, value] of formData.entries()) {
            if (value.trim() !== '') {
                params.append(key, value);
            }
        }

        const queryString = params.toString();
        const url = `${window.location.pathname}?${queryString}`;

        fetch(url, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.text())
        .then(html => {
            container.innerHTML = html;
            container.style.opacity = '1';

            if (updateUrl) {
                window.history.pushState({}, '', url);
            }
        })
        .catch(err => {
            console.error('Erreur filtre AJAX:', err);
            container.style.opacity = '1';
        });
    }

    // 1. Soumission du formulaire
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        pageInput.value = 1; // Retour page 1 lors d'un nouveau filtre
        fetchProducts();
    });

    // 2. Clic sur une catégorie
    document.getElementById('category-list').addEventListener('click', function(e) {
        const btn = e.target.closest('.category-btn');
        if (!btn) return;

        const catSlug = btn.getAttribute('data-category');
        categoryInput.value = catSlug;
        
        // REGLE METIER : Sélectionner une catégorie réinitialise la recherche texte 'q'
        searchInput.value = '';
        pageInput.value = 1;

        // Mise à jour visuelle des boutons catégories
        document.querySelectorAll('.category-btn').forEach(b => {
            b.className = 'category-btn w-full text-left flex items-center gap-2 px-3 py-2 rounded-lg text-sm transition-colors text-stone-600 hover:bg-stone-50';
            const span = b.querySelector('span');
            if (span) span.className = 'w-1.5 h-1.5 rounded-full bg-stone-200';
        });

        btn.className = 'category-btn w-full text-left flex items-center gap-2 px-3 py-2 rounded-lg text-sm transition-colors bg-amber-50 text-amber-700 font-semibold';
        const activeSpan = btn.querySelector('span');
        if (activeSpan) activeSpan.className = 'w-1.5 h-1.5 rounded-full bg-amber-500';

        fetchProducts();
    });

    // 3. Gestion de la pagination asynchrone
    container.addEventListener('click', function(e) {
        const pageLink = e.target.closest('.page-link');
        const resetLink = e.target.closest('.reset-filters-btn');

        if (pageLink) {
            e.preventDefault();
            pageInput.value = pageLink.getAttribute('data-page');
            fetchProducts();
            window.scrollTo({ top: container.offsetTop - 100, behavior: 'smooth' });
        } else if (resetLink) {
            e.preventDefault();
            resetFilters();
        }
    });

    // 4. Réinitialisation complète
    function resetFilters() {
        form.reset();
        categoryInput.value = '';
        pageInput.value = 1;
        searchInput.value = '';

        // Reset visuel catégories
        document.querySelectorAll('.category-btn').forEach((b, index) => {
            if (index === 0) {
                b.className = 'category-btn w-full text-left flex items-center gap-2 px-3 py-2 rounded-lg text-sm transition-colors bg-amber-50 text-amber-700 font-semibold';
                b.querySelector('span').className = 'w-1.5 h-1.5 rounded-full bg-amber-500';
            } else {
                b.className = 'category-btn w-full text-left flex items-center gap-2 px-3 py-2 rounded-lg text-sm transition-colors text-stone-600 hover:bg-stone-50';
                b.querySelector('span').className = 'w-1.5 h-1.5 rounded-full bg-stone-200';
            }
        });

        fetchProducts();
    }

    if (resetBtn) {
        resetBtn.addEventListener('click', resetFilters);
    }

    // 5. Gestion des boutons précédent/suivant du navigateur
    window.addEventListener('popstate', function() {
        location.reload();
    });
});