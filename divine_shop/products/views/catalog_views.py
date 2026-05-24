from django.views.generic import DetailView, TemplateView
from django.views.generic import ListView
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render
from django.views import View
from django.db import models
from divine_shop.products.models import Category
from divine_shop.products.models import Product



class HomeView(TemplateView):
    template_name = "pages/index.html"  # Ta page d'accueil principale

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # On récupère les 4 premières catégories valides en français
        context["categories_populaires"] = (
            Category.objects.exclude(image="")
            .exclude(image__isnull=True)
            .order_by("name")[:4]
        )
        return context

class ProductListView(ListView):
    """
    Vue publique — liste tous les produits disponibles
    Accessible à tout le monde (pas besoin d'être connecté)
    """

    model = Product
    template_name = "products/catalog/product_list.html"
    context_object_name = "products"
    paginate_by = 12  # 12 produits par page

    def get_queryset(self):
        """
        On retourne uniquement les produits disponibles
        Optimisé avec select_related pour éviter les requêtes N+1
        """
        return (
            Product.objects.filter(is_available=True)
            .select_related("category", "seller")
            .prefetch_related("images")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # On passe toutes les catégories pour le menu de filtre
        context["categories"] = Category.objects.all()
        return context


class ProductDetailView(DetailView):
    """
    Vue publique — détail d'un produit
    On utilise le slug dans l'URL au lieu de l'ID (plus propre et SEO)
    """

    model = Product
    template_name = "products/catalog/product_detail.html"
    context_object_name = "product"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return (
            Product.objects.filter(is_available=True)
            .select_related("category", "seller")
            .prefetch_related("images")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Produits similaires — même catégorie, pas le produit actuel
        context["related_products"] = (
            Product.objects.filter(
                category=self.object.category,
                is_available=True,
            )
            .exclude(pk=self.object.pk)
            .prefetch_related("images")[:4]  # maximum 4 produits similaires
        )
        return context


class CategoryProductListView(ListView):
    """
    Vue publique — liste les produits d'une catégorie spécifique
    """

    model = Product
    template_name = "products/catalog/product_list.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        # On récupère la catégorie via son slug dans l'URL
        self.category = Category.objects.get(slug=self.kwargs["slug"])
        return (
            Product.objects.filter(
                category=self.category,
                is_available=True,
            )
            .select_related("category", "seller")
            .prefetch_related("images")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["current_category"] = self.category
        return context
    

class ProductSearchView(View):
    def get(self, request):
        query = request.GET.get("q", "").strip()
        products = []
        categories = []

        if len(query) >= 2:
            products = (
                Product.objects.filter(
                    models.Q(name__icontains=query) |
                    models.Q(description__icontains=query),
                    is_available=True,
                )
                .select_related("category")
                .prefetch_related("images")[:5]
            )

            categories = Category.objects.filter(
                name__icontains=query
            )[:3]

        return render(request, "products/catalog/search_result.html", {
            "products": products,
            "categories": categories,
            "query": query,
        })
