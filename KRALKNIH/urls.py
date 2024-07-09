"""
URL configuration for KRALKNIH project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.contrib.auth.views import LoginView

from accounts.views import SubmittableLoginView, SignUpView, SubmittablePasswordChangeView
from core.views import *
from KRALKNIH import settings #jak je mozny, ze nam to jakoby nenachazi cestu? je to mozny?

admin.site.site_header = 'Král Knih - Administrační panel'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('tags/', include('tags.urls')),
    path('likes/', include('likes.urls')),

    path('accounts/login/', SubmittableLoginView.as_view(), name='login'), 
    path('accounts/signup/', SignUpView.as_view(), name='signup'),         
    path('accounts/password_change/', SubmittablePasswordChangeView.as_view(), name='password_change'),
    path('accounts/', include('django.contrib.auth.urls')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
