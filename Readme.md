# Project Name: Warehouse Management System
This is a `Django-based web application`  using `sqlite3` relational database that serves as a warehouse management system for one of the biggest ready-to-assemble furniture company. The application is designed to help the store keep track of its inventory and manage its stock of products.

# Features
- Upload articles and product configurations in bulk using Json files
- View a list of articles and product configurations
- View product details and stock information
- Sell products by quantity(by default is 1 i.e User can sell a product p1  and the quantity will decrease by 1 and related articles stock wil also decrease as per product config of given product) and update stock levels accordingly

# Installation
- Clone the repository using the command git clone 
```shell
  https://github.com/<username>/<repository_name>.git
  ```
- Install the required dependencies by running 
```shell
  pip install -r requirements.txt
  ```
- Set up the database by running 
```shell
  python manage.py makemigrations
 ```
followed by 
```shell
  python manage.py migrate
 ```
Start the development server using 
```shell
  python manage.py runserver
 ```

# Usage
- admin/ - Django admin panel for managing the application (http://localhost:8000/admin/)
- inventory/ - URL for the inventory management app (http://localhost:8000/inventory/)

# URLs
The project has the following API endpoints:

### Admin (Application) URLS
- admin/ - Django admin panel for managing the application (http://localhost:8000/admin/)
- inventory/ - URL for the inventory management app
---------------------
### Inventory App URLS
- upload-articles/ - Upload articles in bulk using a JSON file (http://localhost:8000/inventory/upload-articles/)
- upload-products-config/ - Upload product configurations in bulk using a JSON file (http://localhost:8000/inventory/upload-products-config/)
- articles/ - List and create articles
```shell
curl -X "GET" http://localhost:8000/inventory/articles/ -H "Content-Type: application/json"
```
- articles/<int:article_id>/ - Retrieve a specific product by ID 
```shell
curl -X "GET" http://localhost:8000/inventory/articles/1/ -H "Content-Type: application/json"
```
- products-config/ - List and create product configurations
```shell
curl -X "GET" http://localhost:8000/inventory/inventory/products-config/ -H "Content-Type: application/json"
```
- products-config/<int:pk>/ - Retrieve, update, and delete a specific product configuration
```shell
curl -X "GET" http://localhost:8000/inventory/products-config/1/ -H "Content-Type: application/json"
```
- products/ - List all products
```shell
curl -X "GET" http://localhost:8000/inventory/products/ -H "Content-Type: application/json"
```
- products/<int:product_id>/ - Retrieve a specific product by ID
```shell
curl -X "GET" http://localhost:8000/inventory/products/14/ -H "Content-Type: application/json"
```
- products/<int:product_id>/sell/ - Sell a specific product and update the stock levels accordingly
```shell
curl -X "PUT" http://localhost:8000/inventory/products/15/sell/ -H "Content-Type: application/json"
```
# Models
## Article
- id - Primary key for the article model
- name - Name of the article
- stock - Current stock level of the article
## ProductConfig
- name - Name of the product configuration
- articles - Many-to-many relationship with the Article model through the ProductArticle model
## ProductArticle
- product - Foreign key to the ProductConfig model
- article - Foreign key to the Article model
- quantity - Quantity of the article needed for the product configuration

- 