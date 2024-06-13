"""
URL configuration for first_pro project.

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
import os
from django.contrib import admin
from django.urls import path, include
from first_app import views
from first_app.user_register import user_register  # Import from the first_app package
from first_app.models import Service
from first_app.services_views import vehicle_list_with_service


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', include('first_app.urls')),
    path('login',views.login_user,name = 'login'),
    #path("index/", views.index, name="index"),
    path('clients/', views.purchased_clients, name='clients'),
    path('clients/register', views.register, name='register'),
    path('user_register/', user_register, name='user_register'),
    path('my_view/', views.my_view, name='my_view'),
    path('logout/', views.logout_view, name='logout'),  # Name your URL pattern 'logout'
    path('service/', vehicle_list_with_service, name='service'),


    ]






"""
dublin@1234

   """ 