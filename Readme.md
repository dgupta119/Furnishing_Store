# Project Name: Warehouse Management System
This is a `Django-based web application`  using `sqlite3` relational database that serves as a warehouse management system for one of the biggest ready-to-assemble furniture company. The application is designed to help the store keep track of its inventory and manage its stock of products.

# Features
- Upload articles and product configurations in bulk using Json files
- View a list of articles and product configurations
- View product details and stock information
- Sell products by quantity(by default is 1 i.e User can sell a product p1  and the quantity will decrease by 1 and related articles stock wil also decrease as per product config of given product) and update stock levels accordingly

# Installation
- These instructions are on assumption that you already have installed `pyhton` and `pip` in your system.
- Install the required dependencies by running 
```shell
  pip install -r requirements.txt
  ```
- Set up the database by running (this command will create equivalent SQl queries)
```shell
  python manage.py makemigrations 
 ```
- followed by (this will exceute the SQL queries which were created in prev step)
```shell
  python manage.py migrate
 ```
- Start the development server using 
```shell
  python manage.py runserver
 ```
- By default, it will start the server at localhost (127.0.0.1) and at port number (8000)
- To verify, if your server is running open this [http://localhost:8000/admin/](http://localhost:8000/admin/)  in your web browser and you should be greeted by login page.
- To access admin board please create a superuser by running following command
```shell
  python manage.py createsuperuser
 ```
# How to Use?
- The system is currently operational, and we have successfully created the database. Now, it's time to upload some data so that we can utilize it and perform various operations on it.
- To upload inventory run
  - upload-articles/ - Upload articles in bulk using a JSON file (http://localhost:8000/inventory/upload-articles/)
- To upload products run
  - upload-products-config/ - Upload product configurations in bulk using a JSON file (http://localhost:8000/inventory/upload-products-config/)

# URLs
The project has the following API endpoints:

### Admin (Application) URLS
- admin/ - Django admin panel for managing the application (http://localhost:8000/admin/)
- inventory/ - URL for the inventory management app
---------------------
### Inventory App URLS
- upload-articles/ - Upload articles in bulk using a JSON file (http://localhost:8000/inventory/upload-articles/)
- upload-products-config/ - Upload product configurations in bulk using a JSON file (http://localhost:8000/inventory/upload-products-config/)
### Using Browser:
- click [here](http://localhost:8000/urls/)
### Using Curl request:
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