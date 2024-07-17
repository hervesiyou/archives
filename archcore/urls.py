 
from django.urls import path
from . import views
 

urlpatterns = [ 
    path('', views.listcom, name="listcom"),
    path('lfam/<int:id>', views.listfamilles, name="listfamilles"),
    path('sf/<int:id>', views.show_famille, name="show_famille"),
   
]