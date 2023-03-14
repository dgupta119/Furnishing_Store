from django.contrib import admin

from .models import Article, ProductArticle, ProductConfig


class ProductArticleInline(admin.TabularInline):
    model = ProductArticle
    extra = 1


class ArticleAdmin(admin.ModelAdmin):
    model = Article
    list_display = ("id", "name", "stock")


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductArticleInline]
    list_display = ("name",)


admin.site.register(Article, ArticleAdmin)
admin.site.register(ProductConfig, ProductAdmin)
