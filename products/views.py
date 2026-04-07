from django.views.generic import DetailView
from django.views.generic import ListView

from .models import Product


class ProductListView(ListView):
    """Liste de tous les produits"""

    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 12  # 12 produits par page

    def get_queryset(self):
        return Product.objects.filter(is_available=True).select_related("category")


class ProductDetailView(DetailView):
    """Détail d'un produit"""

    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"
    slug_url_kwarg = "slug"
