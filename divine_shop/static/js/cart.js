document.addEventListener("DOMContentLoaded", function () {

  const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]")?.value || "";

  document.querySelectorAll(".add-to-cart-btn").forEach(btn => {
    btn.addEventListener("click", function () {
      const productId = this.dataset.productId;

      // Feedback visuel immédiat
      this.disabled = true;
      this.innerHTML = '<span class="material-symbols-outlined text-[14px]">check</span> Ajouté';
      this.classList.add("bg-emerald-600");
      this.classList.remove("bg-stone-900", "hover:bg-amber-700");

      fetch("/orders/cart/add/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({ product_id: productId, quantity: 1 }),
      })
      .then(res => res.json())
      .then(data => {
        if (data.status === "success") {
          // Met à jour le compteur panier dans la navbar
          const cartCount = document.getElementById("cart-count");
          if (cartCount && data.cart_total) {
            cartCount.textContent = data.cart_total;
          }
        }
        // Remet le bouton après 2s
        setTimeout(() => {
          this.disabled = false;
          this.innerHTML = '<span class="material-symbols-outlined text-[14px]">shopping_bag</span> Ajouter';
          this.classList.remove("bg-emerald-600");
          this.classList.add("bg-stone-900", "hover:bg-amber-700");
        }, 2000);
      })
      .catch(() => {
        this.disabled = false;
        this.innerHTML = '<span class="material-symbols-outlined text-[14px]">shopping_bag</span> Ajouter';
        this.classList.remove("bg-emerald-600");
        this.classList.add("bg-stone-900");
      });
    });
  });

});