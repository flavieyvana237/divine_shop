from django.urls import path

from ..divine_shop.products import views

app_name = "products"

urlpatterns = [
    path("", views.ProductListView.as_view(), name="product_list"),
    path("<slug:slug>/", views.ProductDetailView.as_view(), name="product_detail"),
]
