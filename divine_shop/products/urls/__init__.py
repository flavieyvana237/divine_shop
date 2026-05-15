from django.urls import include
from django.urls import path

urlpatterns = [
    path("boutique/", include(("products.urls.catalog_urls", "products"))),
]
