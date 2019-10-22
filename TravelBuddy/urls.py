"""TravelBuddy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from TravelBuddyApp import views

urlpatterns = [
    path('jointravelplan/<id>', views.jointravelplan),
    path('travels/destination/<id>', views.showdestination),
    path('add', views.add),
    path('travels/add',  views.addpage),
    path('travels', views.travels),
    path('logout', views.logout),
    path('login', views.login),
    path('register', views.register),
    path('', views.index),
    path('admin/', admin.site.urls),
]
