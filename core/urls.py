from django.urls import path

from . import views
from .views import BooksView

app_name = 'core'

urlpatterns = [
    path('', views.home),
    path('about/', views.show_about, name='about'),
    path('books/', BooksView.as_view(), name='books'),
    #path('books/<int:id>/', views.book_detail), #API maybe
]
