import json
import math
import os
import re
from collections import defaultdict

Inventory = {
    "inventory": [
        {"art_id": "1", "name": "leg", "stock": "12"},
        {"art_id": "2", "name": "screw", "stock": "17"},
        {"art_id": "3", "name": "seat", "stock": "2"},
        {"art_id": "4", "name": "table top", "stock": "1"},
    ]
}

Product = {
    "products": [
        {
            "name": "Dining Chair",
            "contain_articles": [
                {"art_id": "1", "amount_of": "4"},
                {"art_id": "2", "amount_of": "8"},
                {"art_id": "3", "amount_of": "1"},
            ],
        },
        {
            "name": "Dinning Table",
            "contain_articles": [
                {"art_id": "1", "amount_of": "4"},
                {"art_id": "2", "amount_of": "8"},
                {"art_id": "4", "amount_of": "1"},
            ],
        },
    ]
}


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Warehouse:
    _articles_from_inventory: dict
    _product_config: dict

    @staticmethod
    def modified_product_name(name):
        return re.sub(r"\s+", "", name).lower() if name else None

    def __init__(self, inventory=None, products=None):
        self._products_config = defaultdict()
        self._articles_from_inventory = defaultdict()
        self._products_in_inventory = defaultdict()
        if inventory:
            self._articles_from_inventory = self._processed_inventory(
                inventory.get("inventory")
            )
        if products:
            self._products_config = self._processed_product(products.get("products"))
        self._calculate_products_in_inventory()

    def get_product(self, name: str = None):
        product_name_key = Warehouse.modified_product_name(name)
        if product_name_key and product_name_key in self._products_in_inventory:
            return self._products_in_inventory[product_name_key]
        return list(self._products_in_inventory.values())

    def sell_product(self, name: str, quantity: int = None):
        # update the inventory after removing this product
        product_name_key = Warehouse.modified_product_name(name)
        if product_name_key and product_name_key not in self._products_in_inventory:
            return "Product can not be sold bc it's not present in Inventory"
        self._update_inventory(product_name_key, quantity)
        return

    def upload_inventory(self, file_path):
        with open(file_path) as f:
            inventory = json.load(f)

        articles_from_inventory_after_uploading = self._processed_inventory(
            inventory.get("inventory")
        )

        for article_id in articles_from_inventory_after_uploading:
            article_data = articles_from_inventory_after_uploading[article_id]
            if article_id in self._articles_from_inventory:
                self._articles_from_inventory[article_id][
                    "stock"
                ] = self._articles_from_inventory[article_id][
                    "stock"
                ] + article_data.get(
                    "stock"
                )
            else:
                self._articles_from_inventory[article_id] = article_data

        self._calculate_products_in_inventory()

    def upload_products(self, file_path):
        with open(file_path) as f:
            products = json.load(f)

        new_product_config_after_uploading = self._processed_product(
            products.get("products")
        )
        self._products_config = {
            **self._products_config,
            **new_product_config_after_uploading,
        }
        self._calculate_products_in_inventory()

    def _processed_inventory(self, inventory):
        articles_from_inventory = defaultdict()
        for article in inventory:
            articles_from_inventory[article.get("art_id")] = {
                "name": article.get("name"),
                "stock": int(article.get("stock")),
            }
        return articles_from_inventory

    def _processed_product(self, products):
        products_config = defaultdict()
        for product in products:
            products_config[Warehouse.modified_product_name(product.get("name"))] = {
                "name": product.get("name"),
                "contain_articles": product.get("contain_articles"),
            }
        return products_config

    def _calculate_products_in_inventory(self):
        for product in self._products_config:
            product_name = self._products_config[product]["name"]
            contain_articles = self._products_config[product]["contain_articles"]
            number_of_products_can_create = math.inf
            for article in contain_articles:
                if article.get("art_id") in self._articles_from_inventory:
                    number_of_products_can_create = min(
                        number_of_products_can_create,
                        int(
                            self._articles_from_inventory[article.get("art_id")].get(
                                "stock"
                            )
                        )
                        // int(article.get("amount_of")),
                    )
            self._products_in_inventory[product] = {
                "name": product_name,
                "quantity": number_of_products_can_create,
            }

    def _update_inventory(self, product_name_key, quantity_to_be_sold=None):

        contain_articles = self._products_config[product_name_key]["contain_articles"]
        current_quantity_of_product = self._products_in_inventory[product_name_key][
            "quantity"
        ]

        quantity_to_be_sold = (
            current_quantity_of_product
            if quantity_to_be_sold is None
            else quantity_to_be_sold
        )

        if quantity_to_be_sold > current_quantity_of_product:
            quantity_to_be_sold = current_quantity_of_product

        if quantity_to_be_sold == 0:
            return

        self._products_in_inventory[product_name_key]["quantity"] = (
            current_quantity_of_product - quantity_to_be_sold
        )  # update the product quantity
        if self._products_in_inventory[product_name_key]["quantity"] == 0:
            del self._products_in_inventory[product_name_key]
        for article in contain_articles:  # update  inventory
            self._articles_from_inventory[article.get("art_id")]["stock"] = int(
                self._articles_from_inventory[article.get("art_id")]["stock"]
            ) - quantity_to_be_sold * int(article.get("amount_of"))
            if self._articles_from_inventory[article.get("art_id")]["stock"] == 0:
                del self._articles_from_inventory[article.get("art_id")]


if __name__ == "__main__":
    warehouse_obj = Warehouse()
    print(warehouse_obj.get_product())
    print(warehouse_obj.sell_product("Dining Chair", 1))
    print(warehouse_obj.get_product())
    products_config_dir = os.path.join(BASE_DIR, "products.json")
    warehouse_obj.upload_products(products_config_dir)
    inventory_dir = os.path.join(BASE_DIR, "inventory.json")
    warehouse_obj.upload_inventory(inventory_dir)
    print(warehouse_obj.get_product())
