import os

from django.shortcuts import redirect, render
from django.views import View
from rest_framework import generics
from rest_framework.parsers import JSONParser

from inventory.models import Article, ProductConfig
from inventory.serializers import (ProductConfigUploadSerializer,
                                   ProductSerializer)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

from inventory.logger import setup_logger

# Setup logging
logger = setup_logger(__name__, "products config")


class ProductConfigUploadView(View):
    """
    A view to upload a JSON file containing products configuration data.
    """

    def get(self, request):
        """
        Handles GET requests to retrieve the upload page.

        :param request: The incoming HTTP request object.
        :return: A rendered HTML template for the upload page.
        """
        products_config_dir = os.path.join(BASE_DIR, "../../assignment/products.json")
        with open(products_config_dir, "r") as f:
            products_config_json = f.read()
        return render(
            request,
            "upload.html",
            {"view_name": "Products Config", "products_json": products_config_json},
        )

    def post(self, request):
        """
        Handles POST requests to upload the JSON file and update the database.

        :param request: The incoming HTTP request object.
        :return: A redirect to the admin index page.
        """
        file = request.FILES["file"]
        data = JSONParser().parse(file)

        serializer = ProductConfigUploadSerializer(
            data=data.get("products", []), many=True
        )
        serializer.is_valid(raise_exception=True)

        for product_data in serializer.validated_data:
            product_config_obj, _ = ProductConfig.objects.get_or_create(
                name=product_data["name"]
            )
            product_config_obj.articles.clear()

            for article_data in product_data["contain_articles"]:
                article = Article.objects.get(id=article_data["art_id"])
                quantity = int(article_data["amount_of"])
                product_config_obj.articles.add(
                    article, through_defaults={"quantity": quantity}
                )

            product_config_obj.save()

        return redirect("admin:index")


class ProductConfigListCreateView(generics.ListCreateAPIView):
    """
    A view to list and create product configurations.
    """

    queryset = ProductConfig.objects.all()
    serializer_class = ProductSerializer


class ProductConfigRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    A view to retrieve, update, and destroy product configurations.
    """

    queryset = ProductConfig.objects.all()
    serializer_class = ProductSerializer
