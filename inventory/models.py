from django.db import models


class Article(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=100)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class ProductConfig(models.Model):
    name = models.CharField(max_length=100)
    articles = models.ManyToManyField(Article, through="ProductArticle")

    def __str__(self):
        return f"{self.name}"


class ProductArticle(models.Model):
    product = models.ForeignKey(ProductConfig, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} - {self.article.name} ({self.quantity})"
