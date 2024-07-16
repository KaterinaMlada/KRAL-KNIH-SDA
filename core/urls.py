from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.BooksView.as_view(), name="books"),
    path('books/<pk>/', views.BookDetailView.as_view(), name="book_detail"),
    path('category/<int:category_id>/', views.BooksByCategoryView.as_view(), name='books_by_category'), 

    path('cart/', views.cart, name="cart"),
    path('add-to-cart/<int:book_id>/', views.add_to_cart, name="add_to_cart"),
    path('update-cart-item/<int:book_id>/<str:action>/', views.update_cart_item, name="update_cart_item"),
    path('remove-from-cart/<int:book_id>/', views.remove_from_cart, name="remove_from_cart"),

    path('checkout/', views.checkout, name="checkout"),

    path('about/', views.show_about, name='about'),
]
