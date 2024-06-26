Toto je finalni projekt.

Jedna se o e-shop s knihami.

Zadání:

Online store with an administrator panel
-
Brief description of the system

As part of the project, create an application, that allows you to add products to the store through the administrative panel, enable user registration and logging in as well as placing orders.

Main system functions
-
Login panel. Admin:

Adding categories for products.

Category tree overview.

Adding products.

Product list + edition. 


User:
-
Registration.

List of products.

Product table with pagination.

Viewing the weather for the user's city.

General Guidelines
-
Build the website using Django. Introduce the division into models, views and controllers in the application and place an appropriate logic in each of them. Secure access to the application and its functionalities using django.contrib.auth.

Basic entities (proposal)
-
Category
-
name

parent categories and children categories
(tree placement)

User account

login (email)

password (hash)

city

address (country, city, street, ZIP code)

logotype / thumbnail / avatar

role (ADMIN/USER - entity)

preferred communication channel (mail / email)

Product
-
title

description

thumbnail (url)

category (entity)

price

product type (enum)

author (entity)

Order line
-
Product (entity)

Number of products

Product price

Order
-
User name

Total cost

Delivery address

User address

Date of submission

Order lines (entity)

Client (entity)

Status (enum)

Author
-
Name

Surname

Role
-
Role name

Cart (not entity)
-
Order lines

Functionalities
-
ADMIN: Adding a category

category name

parent id

Category tree overview
-
category search

option to drag categories (change position)

Adding a product
-
name

description

picture url

availability

price

product type (dropdown)

category (dropdown)

author (dropdown)

Product list
-
list of all added products with their details

button to edit a product

product search

USER:
-
User registration

entering data into form fields + validation of these fields

Log in
-
User login option (after prior registration)

possibility for a user to log out

Weather widget
-
displaying weather based on a city of the currently logged in user

Products list
-
display products as a list or as a grid

product search

add product to cart

Table with products (using Ajax on GET query and inserting parameters into the url)
-
displaying products in a table with pagination

sorting products in the table

Ajax product search

adding products to the cart

Cart
-
displaying products added to the cart

option to order products from the cart -> leads to a static thank you page and reduces product availability

Additional tasks and extensions
-
edit a user account (data)

overview of user orders (from a user and admin level)

add the author in the admin panel

Additional requirements
-
it is necessary to ensure an aesthetic and functional way of presenting data

data collected from users should be pre-validated