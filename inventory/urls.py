from django.contrib import admin
from django.urls import path

from inventory.views import (ArticleListCreateView, ArticleUploadView,
                             ProductConfigListCreateView,
                             ProductConfigRetrieveUpdateDestroyView,
                             ProductConfigUploadView, ProductSellView,
                             ProductView)

app_name = "inventory"

# Set the admin site header
admin.site.site_header = "IKEA Warehouse"

# Define the urlpatterns for the inventory app
urlpatterns = [
    # Path to upload new articles
    path("upload-articles/", ArticleUploadView.as_view(), name="upload-articles"),
    # Path to upload new product configurations
    path(
        "upload-products-config/",
        ProductConfigUploadView.as_view(),
        name="upload-products-config",
    ),
    # Path to list and create articles
    path("articles/", ArticleListCreateView.as_view(), name="article-list-create"),
    # Path to list and create product configurations
    path(
        "products-config/",
        ProductConfigListCreateView.as_view(),
        name="product-config-list-create",
    ),
    # Path to retrieve, update, and delete a specific product configuration
    path(
        "products-config/<int:pk>/",
        ProductConfigRetrieveUpdateDestroyView.as_view(),
        name="product-config-retrieve-update-destroy",
    ),
    # Path to list all products
    path("products/", ProductView.as_view(), name="product-list"),
    # Path to retrieve and update a specific product
    path("products/<int:product_id>/", ProductView.as_view(), name="product-details"),
    # Path to sell a specific product
    path(
        "products/<int:product_id>/sell/",
        ProductSellView.as_view(),
        name="product-sell",
    ),
]
