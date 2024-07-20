 
from django.urls import path
from . import views
 

urlpatterns = [ 
    path('', views.listcom, name="listcom"),
    path('lfam/<int:id>', views.listfamilles, name="listfamilles"),
    path('sf/<int:id>', views.show_famille, name="show_famille"),
    path('sa/<int:id>', views.show_association, name="show_association"),
    path('sc/<int:id>', views.show_communaute, name="show_communaute"),
    path('nc/', views.add_communaute, name="add_communaute"),
    path('na/', views.add_association, name="add_association"),
    path('nf/', views.add_famille, name="add_famille"),
   
]