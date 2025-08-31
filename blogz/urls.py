"""
URL configuration for blogz project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf import settings
from django.views.generic import TemplateView
from django.conf.urls.static import static
from MyAuth.views import reset_password_confirm
from MyApp.views import home 
from MyAuth.views import custom_404_view


urlpatterns = [
    path('',home,name='home'),
    path('admin/', admin.site.urls),
    path('myauth/', include('MyAuth.urls')),
    path('myapp/', include('MyApp.urls')),
    # for OAuth :
    path('accounts/', include('allauth.urls')), 
    # for editor :
    path('tinymce/', include('tinymce.urls')),
    # djoser :
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),  # if using token-based
    path('activate/', TemplateView.as_view(template_name='activate.html'),
         name='activate'),
    path('set-password/', reset_password_confirm, name='set_password'),
    path('auth/', include('djoser.urls.jwt')),
]

handler404 = 'MyAuth.views.custom_404_view'

from django.conf.urls.static import static

# Serve media files (only if DEBUG = True OR temp fix for Render)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom error handler