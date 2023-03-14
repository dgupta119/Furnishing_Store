import json
import os

from django.db import models
from django.db.models import ExpressionWrapper, F, Min
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseNotAllowed, HttpResponseNotFound,
                         JsonResponse)
from django.views import View

from inventory.models import Article, ProductArticle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

from inventory.logger import setup_logger

# Setup logging
logger = setup_logger(__name__, " products ")


class ProductView(View):
    """
    A view to handle product related requests.
    """

    def get(self, request, product_id=None):
        """
        Returns a JSON response containing a list of products and their stock levels.

        If product_id is specified, only the details of that product will be returned.

        :param request: The incoming HTTP request object.
        :param product_id: The id of the product to retrieve.
        :return: A JSON response object containing product data.
        """
        try:
            # Query the database to get the product name and the minimum stock level of all the articles
            data = (
                ProductArticle.objects.values("product_id", "product__name")
                .annotate(
                    article_stock=ExpressionWrapper(
                        Min(F("article__stock") / F("quantity")),
                        output_field=models.IntegerField(),
                    )
                )
                .values("product_id", "product__name", "article_stock")
            )

            # Filter the data based on the specified product_id, if present
            if product_id:
                data = data.filter(product_id=product_id)

            # If no data exists after filtering, return a 404 response
            if not data.exists():
                return HttpResponseNotFound()

            # Convert the query results to the desired response format
            context = {
                "products": [
                    {
                        "id": d["product_id"],
                        "name": d["product__name"],
                        "stock": d["article_stock"],
                    }
                    for d in data
                ]
            }

            # Return the response as a JSON object
            return JsonResponse(context)
        except ValueError:
            # Return a 400 response for invalid requests
            return HttpResponseBadRequest()


DEFAULT_QUANTITY_TO_SELL = 1


class ProductSellView(View):
    """
    A view to handle product sales.
    """

    def put(self, request, product_id):
        """
        Handles PUT requests to sell a product.

        The request body should contain a 'quantity' field indicating the number of products to sell.

        :param request: The incoming HTTP request object.
        :param product_id: The id of the product to sell.
        :return: An HTTP response indicating the success or failure of the sale.
        """
        try:
            # Get all the articles associated with the product
            product_article_entries = ProductArticle.objects.filter(
                product_id=product_id
            )

            # For each article, update its stock level based on the quantity sold
            for entry in product_article_entries:
                article_id = entry.article_id
                quantity = (
                    json.loads(request.body).get("quantity", DEFAULT_QUANTITY_TO_SELL)
                    if request.body
                    else DEFAULT_QUANTITY_TO_SELL
                )
                article = Article.objects.get(id=article_id)
                article.stock -= quantity * entry.quantity
                article.save()

            # Return a success response
            return HttpResponse("Product sold successfully.")
        except (ProductArticle.DoesNotExist, Article.DoesNotExist):
            # Return a 404 response for invalid product or article ids
            return HttpResponseNotFound("Invalid product id or article id.")
        except ValueError:
            # Return a 400 response for invalid quantity values
            return HttpResponseBadRequest("Invalid quantity.")
        except Exception as e:
            # Return a 405 response for other errors
            return HttpResponseNotAllowed("Method not allowed.")
