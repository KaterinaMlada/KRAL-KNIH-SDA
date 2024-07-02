from django.contrib import admin
from django.contrib.admin import ModelAdmin
from core.models import Author, Promotion, Role, Customer, Address, Category, Book, Order, OrderItem, Cart, CartItem #Doplnit prosiim pak



admin.site.register(Author)

admin.site.register(Promotion)

admin.site.register(Role)

admin.site.register(Customer)

admin.site.register(Address)

admin.site.register(Category)

admin.site.register(Book)

admin.site.register(Order)

admin.site.register(OrderItem)

admin.site.register(Cart)

admin.site.register(CartItem)