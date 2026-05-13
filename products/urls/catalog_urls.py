from django.urls import path

from products.views.catalog_views import CategoryProductListView, ProductSearchView
from products.views.catalog_views import ProductDetailView
from products.views.catalog_views import ProductListView

app_name = "catalog"

urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    path("search/", ProductSearchView.as_view(), name="product_search"),
    path("categorie/<slug:slug>/",
        CategoryProductListView.as_view(),
        name="category_products",
    ),
    path("<slug:slug>/", ProductDetailView.as_view(), name="product_detail"),
]

# pour verifier les urls
# python manage.py show_urls | grep products
