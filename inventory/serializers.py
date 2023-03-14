# inventory/serializers.py
from rest_framework import serializers

from .models import Article, ProductArticle, ProductConfig


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"


class ProductArticleSerializer(serializers.ModelSerializer):
    article_name = serializers.CharField(source="name")

    class Meta:
        model = ProductArticle
        fields = ["article_name"]


class ProductSerializer(serializers.ModelSerializer):
    articles = ProductArticleSerializer(many=True, read_only=True)

    class Meta:
        model = ProductConfig
        fields = ["name", "articles"]


class ArticleUploadSerializer(serializers.Serializer):
    art_id = serializers.IntegerField()
    name = serializers.CharField()
    stock = serializers.IntegerField()


class ProductConfigUploadSerializer(serializers.Serializer):
    name = serializers.CharField()
    contain_articles = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField(),  # Or use serializers.IntegerField() if "art_id" is always an integer
        )
    )
