from django.views.generic import DetailView, TemplateView
from django.views.generic import ListView
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render
from django.views import View
from django.db import models
from divine_shop.products.models import Category, Promotion,Product
from divine_shop.users.models import Testimonial 
from django.utils import timezone
from django.db.models import Q





class HomeView(TemplateView):
    template_name = "pages/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()

        # Catégories populaires — avec image uniquement
        context["categories_populaires"] = (
            Category.objects.exclude(image="")
            .exclude(image__isnull=True)
            .order_by("name")[:4]
        )

        # Produits vedettes — is_featured=True, disponibles, avec images
        context["produits_vedettes"] = (
            Product.objects.filter(
                is_featured=True,
                is_available=True,
                stock__gt=0,
            )
            .select_related("category")
            .prefetch_related("images", "promotions")
            .order_by("-created_at")[:8]
        )

        # Nouveautés — produits récents
        context["nouveautes"] = (
            Product.objects.filter(
                is_new=True,
                is_available=True,
                stock__gt=0,
            )
            .select_related("category")
            .prefetch_related("images", "promotions")
            .order_by("-created_at")[:4]
        )

        # Promotion active — une seule à la fois sur la bannière
        context["promotion_active"] = (
            Promotion.objects.filter(
                is_active=True,
                start_date__lte=now,
                end_date__gte=now,
            )
            .prefetch_related("products__images")
            .first()
        )

    
        context["testimonials"] = Testimonial.objects.filter(is_approved=True)

        return context
    




class ProductListView(ListView):
    model = Product
    template_name = "products/catalog/product_list.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        qs = (
            Product.objects.filter(is_available=True)
            .select_related("category", "seller")
            .prefetch_related("images", "promotions")
        )

        # Filtre catégorie
        category_slug = self.request.GET.get("category")
        if category_slug:
            qs = qs.filter(category__slug=category_slug)

        # Filtre prix
        price_min = self.request.GET.get("price_min")
        price_max = self.request.GET.get("price_max")
        if price_min:
            qs = qs.filter(price__gte=price_min)
        if price_max:
            qs = qs.filter(price__lte=price_max)

        # Filtre disponibilité
        only_available = self.request.GET.get("available")
        if only_available:
            qs = qs.filter(stock__gt=0)

        # Filtre nouveautés
        only_new = self.request.GET.get("is_new")
        if only_new:
            qs = qs.filter(is_new=True)

        # Filtre vedettes
        only_featured = self.request.GET.get("is_featured")
        if only_featured:
            qs = qs.filter(is_featured=True)

        # Recherche par nom ou description
        search = self.request.GET.get("q")
        if search:
            qs = qs.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )

        return qs

    def get_template_names(self):
        # Si c'est une requête AJAX/Fetch, on renvoie uniquement la grille
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            return ["products/catalog/product_grid.html"]
        return [self.template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["current_filters"] = self.request.GET
        context["current_category"] = self.request.GET.get("category", "")
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
