import json
import os

from django.db.models import Min
from django.test import Client, TestCase
from django.urls import NoReverseMatch, reverse

from inventory.models import Article, ProductArticle, ProductConfig

DEFAULT_QUANTITY_TO_SELL = 1


class ProductViewTestCase(TestCase):
    def setUp(self):
        _setup()

    def test_get_all_products(self):
        client = Client()
        response = self.client.get(reverse("inventory:product-list"))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["products"]), 2)

    def test_get_product_by_id(self):
        client = Client()
        response = self.client.get(reverse("inventory:product-details", args=[1]))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["products"][0]["id"], 1)
        self.assertEqual(data["products"][0]["name"], "Dining Chair")
        self.assertEqual(data["products"][0]["stock"], 2)

    def test_get_product_by_invalid_id(self):
        client = Client()
        response = self.client.get(reverse("inventory:product-details", args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_get_product_with_error(self):
        client = Client()
        url = None
        with self.assertRaises(NoReverseMatch):
            url = reverse("inventory:product-details", args=["abc"])
        response = client.get(url)
        self.assertEqual(response.status_code, 404)


class ProductSellViewTestCase(TestCase):
    def setUp(self):
        _setup()

    def test_product_sell_view_with_valid_product_id(self):
        client = Client()
        product_id = ProductConfig.objects.first().id
        initial_stock = Article.objects.first().stock
        response = client.put(
            reverse("inventory:product-sell", args=[product_id]),
            content_type="application/json",
        )

        # Check that response is successful
        self.assertEqual(response.status_code, 200)
        # Check that stock has been updated
        self.assertEqual(
            Article.objects.first().stock,
            initial_stock
            - ProductArticle.objects.filter(product_id=product_id).values()[0][
                "quantity"
            ]
            * ProductArticle.objects.filter(product_id=product_id).aggregate(
                min_quantity=Min("quantity")
            )["min_quantity"],
        )

    def test_product_sell_view_with_invalid_product_id(self):
        client = Client()
        product_id = "invalid_id"
        url = None
        with self.assertRaises(NoReverseMatch):
            url = reverse("inventory:product-sell", args=[product_id])
        response = client.put(url, content_type="application/json")

        # Check that response is a 404
        self.assertEqual(response.status_code, 404)

    def test_product_sell_view_with_invalid_quantity(self):
        client = Client()
        product_id = ProductConfig.objects.first().id
        response = client.put(
            reverse("inventory:product-sell", args=[product_id]),
            data={"quantity": "invalid_quantity"},
            content_type="application/json",
        )

        # Check that response is a 400
        self.assertEqual(response.status_code, 405)

    def test_product_sell_view_with_no_request_body(self):
        client = Client()
        product_id = ProductConfig.objects.first().id
        initial_stock = Article.objects.first().stock
        response = client.put(
            reverse("inventory:product-sell", args=[product_id]),
            content_type="application/json",
        )

        # Check that response is successful
        self.assertEqual(response.status_code, 200)
        # Check that stock has been updated by the default quantity
        self.assertEqual(
            Article.objects.first().stock,
            initial_stock
            - DEFAULT_QUANTITY_TO_SELL
            * ProductArticle.objects.filter(product_id=product_id).values()[0][
                "quantity"
            ],
        )

    def test_product_sell_view_with_invalid_request_method(self):
        client = Client()
        product_id = ProductConfig.objects.first().id
        response = client.get(
            reverse("inventory:product-sell", args=[product_id]),
            content_type="application/json",
        )

        # Check that response is a 405
        self.assertEqual(response.status_code, 405)


def _setup():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    prodcuts_json = os.path.join(base_dir, "../assignment/products.json")
    inventory_json = os.path.join(base_dir, "../assignment/inventory.json")

    with open(inventory_json) as f:
        inventory_data = json.load(f)

        # Create Article objects from inventory data
    for item in inventory_data["inventory"]:
        Article.objects.create(
            id=item["art_id"], name=item["name"], stock=item["stock"]
        )

        # Load product data from json file
    with open(prodcuts_json) as f:
        product_data = json.load(f)

        # Create ProductConfig objects and their corresponding ProductArticle objects from product data
    for item in product_data["products"]:
        product = ProductConfig.objects.create(name=item["name"])
        for article in item["contain_articles"]:
            ProductArticle.objects.create(
                product=product,
                article_id=article["art_id"],
                quantity=article["amount_of"],
            )
