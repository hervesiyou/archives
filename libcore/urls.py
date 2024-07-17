 
from django.urls import path
from . import views
 

urlpatterns = [ 
    path('', views.listlibs, name="listlibs"),
    path('lbs/<int:id>', views.listbooks, name="listbooks"),
    path('sb/<int:id>', views.show_book, name="show_book"),
   
]