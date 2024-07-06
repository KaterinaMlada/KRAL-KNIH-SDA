from django.contrib import admin
from django.contrib.admin import ModelAdmin
from core.models import Author, Promotion, Role, Customer, Address, Category, Book, Order, OrderItem, Cart, CartItem #Doplnit prosiim pak


@admin.register(Book)
class BookAdmin(ModelAdmin):
    list_display = ['title', 'unit_price']
    list_editable = ['unit_price']
    list_per_page = 15


@admin.register(Customer)
class CustomerAdmin(ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    list_per_page = 10


admin.site.register(Author)

admin.site.register(Promotion)

admin.site.register(Role)

admin.site.register(Address)

admin.site.register(Category)

admin.site.register(Order)

admin.site.register(OrderItem)

admin.site.register(Cart)

admin.site.register(CartItem)
