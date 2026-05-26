from django.urls import include, path
from divine_shop.products.views.catalog_views import HomeView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("boutique/", include(("products.urls.catalog_urls", "products"))),
]
