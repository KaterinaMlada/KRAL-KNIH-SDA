from django.urls import path
from . import views
from .views import cart_count

app_name = 'core'

urlpatterns = [
    path('', views.BooksView.as_view(), name="books"),
    path('books/<pk>/', views.BookDetailView.as_view(), name="book_detail"),
    
    path('category/<int:category_id>/', views.BooksByCategoryView.as_view(), name='books_by_category'), 

    path('cart/', views.cart, name="cart"),
    path('add-to-cart/<int:book_id>/', views.add_to_cart, name="add_to_cart"),
    path('add-to-cart-detail/<int:book_id>/', views.add_to_cart_detail, name="add_to_cart_detail"),
    path('update-cart-item/<int:book_id>/<str:action>/', views.update_cart_item, name="update_cart_item"),
    path('remove-from-cart/<int:book_id>/', views.remove_from_cart, name="remove_from_cart"),
    path('cart/count/', cart_count, name='cart_count'),
    
    path('checkout/', views.checkout, name="checkout"),

    path('about/', views.show_about, name='about'),


]
