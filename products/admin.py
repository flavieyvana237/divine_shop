from django.contrib import admin

from .models import Category
from .models import Product
from .models import ProductImage


class ProductImageInline(admin.TabularInline):
    """
    Permet de gérer les images directement
    depuis la page d'un produit — sans aller
    dans un admin séparé
    """

    model = ProductImage
    extra = 1  # nombre de champs vides affichés par défaut
    fields = ["image", "is_main", "order"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "created_by"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]
    readonly_fields = ["created_at"]  # ← on ne peut pas modifier la date


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "seller", "price", "stock", "is_available"]
    list_filter = ["category", "is_available", "seller"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ["category"]
    readonly_fields = ["created_at", "updated_at"]  # ← dates non modifiables
    inlines = [ProductImageInline]  # ← images gérées directement ici


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ["product", "is_main", "order"]
    list_filter = ["is_main"]
    raw_id_fields = ["product"]
