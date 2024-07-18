from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.db.models import Count
from core.models import *



@admin.register(Author)
class AuthorAdmin(ModelAdmin):
    search_fields = ['first_name', 'last_name']
    list_display = ['last_name', 'first_name']


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ['title', 'books_count']
    search_fields = ['title']

    def books_count(self, category):
        return category.books_count

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(books_count=Count('book'))

"""
class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    extra = 0
    min_num = 0
    model = TaggedItem
"""

@admin.register(Book)
class BookAdmin(ModelAdmin):
    autocomplete_fields = ['authors']
    prepopulated_fields = {
        'slug': ['title']
    }
    list_display = ['title', 'unit_price', 'category']
    list_editable = ['unit_price']
    list_filter = ['category']
    list_per_page = 15
    search_fields = ['title']

    @admin.display(ordering='inventory')
    def inventory_status(self, book):
        if book.inventory < 5:
            return 'Low'
        return 'OK'


@admin.register(Customer)
class CustomerAdmin(ModelAdmin):
    list_display = ['last_name', 'first_name', 'membership',]
    list_editable = ['membership']
    list_filter = ['membership']
    list_per_page = 10
    search_fields = ['last_name', 'first_name']


class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['book']
    extra = 0
    min_num = 1
    model = OrderItem


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    list_display = ['id', 'customer', 'placed_at', 'payment_status',]
    list_editable = ['payment_status']
    list_filter = ['payment_status']
    list_per_page = 10
    ordering = ['placed_at', 'customer']
