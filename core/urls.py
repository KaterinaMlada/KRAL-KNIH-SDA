from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [

    path('', views.BooksView.as_view(), name="books"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('about/', views.show_about, name='about'),

    #path('books/<int:id>/', views.book_detail), #API maybe
]
