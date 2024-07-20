"""
URL configuration for archives project.

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
from coreapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('com/<int:id>', views.show_com, name="show_com"),
     
    path('login', views.log_user, name="login"),
    path('logout', views.log_out, name="logout"),
    
     path('us/', include('coreapp.urls')),
     path('ar/', include('archcore.urls')),
     path('li/', include('libcore.urls')),
     path('mar/', include('marketcore.urls')),
]
