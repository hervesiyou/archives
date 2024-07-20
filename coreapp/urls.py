 
from django.urls import path
from . import views
 

urlpatterns = [ 
    path('new/', views.add_user, name="add_user"),
    path('ngal/', views.add_galerie, name="add_galerie"),
    path('ga/<int:id>', views.show_galerie, name="show_galerie"),
    path('u/<int:id>', views.show_user, name="show_user"),
    
]