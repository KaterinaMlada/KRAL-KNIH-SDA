from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home),
    path('about/', views.show_about),
    path('books/', views.book_list),
    path('books/<int:id>/', views.book_detail),
]
