import os

from django.shortcuts import redirect, render
from django.views import View
from rest_framework import generics

from inventory.models import Article
from inventory.serializers import ArticleSerializer, ArticleUploadSerializer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
from rest_framework.parsers import JSONParser

from inventory.logger import setup_logger

# Setup logging
logger = setup_logger(__name__, " articles ")


class ArticleUploadView(View):
    """
    A view to upload articles from a JSON file.
    """

    def get(self, request):
        inventory_dir = os.path.join(BASE_DIR, "../../assignment/inventory.json")
        with open(inventory_dir, "r") as f:
            articles_json = f.read()
        return render(
            request,
            "upload.html",
            {"view_name": "Articles", "articles_json": articles_json},
        )

    def post(self, request):
        """
        Handles POST requests to upload articles from a JSON file.

        The request body should contain a 'file' field indicating the JSON file to upload.

        :param request: The incoming HTTP request object.
        :return: A redirect to the admin index page.
        """
        file = request.FILES["file"]
        data = JSONParser().parse(file)

        serializer = ArticleUploadSerializer(data=data.get("inventory", []), many=True)
        serializer.is_valid(raise_exception=True)

        for article_data in serializer.validated_data:
            article_obj, created = Article.objects.get_or_create(
                id=article_data["art_id"]
            )

            if not created:
                article_obj.stock += article_data["stock"]
            else:
                article_obj.name = article_data["name"]
                article_obj.stock = article_data["stock"]
            article_obj.save()

        return redirect("admin:index")


class ArticleListCreateView(generics.ListCreateAPIView):
    """
    A view to list and create articles.
    """

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
