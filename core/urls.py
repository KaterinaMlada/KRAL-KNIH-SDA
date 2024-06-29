from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home),
    path('about/', views.show_about)
]
