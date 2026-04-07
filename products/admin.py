from django.contrib import admin

from .models import Category
from .models import Product
from .models import ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "price", "stock", "is_available"]
    list_filter = ["category", "is_available"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ["category"]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ["product", "is_main", "order"]
    list_filter = ["is_main"]
    raw_id_fields = ["product"]
