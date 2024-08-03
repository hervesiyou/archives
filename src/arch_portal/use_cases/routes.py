 
from django.urls import path
import arch_portal.use_cases.marche_controller as marche
import arch_portal.use_cases.librairie_controller as librairie
import arch_portal.use_cases.membre_controller as membre
import arch_portal.use_cases.communaute_controller as communaute
import arch_portal.use_cases.famille_controller as famille
import arch_portal.use_cases.core_controller as core
 

urlpatterns = [ 
    path('lfam/<int:id>', famille.listfamilles, name="listfamilles"),
    path('sf/<int:id>', famille.show_famille, name="show_famille"),
    path('nf/', famille.add_famille, name="add_famille"),
]

urlpatterns += [ 
    path('', core.index, name="index"),
]
urlpatterns += [ 
    path('lcom', communaute.listcom, name="listcom"),
    path('sa/<int:id>', communaute.show_association, name="show_association"),
    path('sc/<int:id>', communaute.show_communaute, name="show_communaute"),
    path('nc/', communaute.add_communaute, name="add_communaute"),
    path('na/', communaute.add_association, name="add_association"),
    path('ngal/', communaute.add_galerie, name="add_galerie"),
    path('ga/<int:id>', communaute.show_galerie, name="show_galerie"),
]

urlpatterns += [ 
    path('u/<int:id>', membre.show_user, name="show_user"),
    path('new/', membre.add_user, name="add_user"),
    path('u/login', membre.log_user, name="login"),
    path('u/logout', membre.log_out, name="logout"),
    path('u/sign', membre.subscribe, name="subscribe"),
    path('u/home', membre.show_user_home, name="home"),
    
]

urlpatterns += [ 
    path('libs', librairie.listlibs, name="listlibs"),
    path('lbs/<int:id>', librairie.listbooks, name="listbooks"),
    path('sb/<int:id>', librairie.show_book, name="show_book"),
    path('ab/', librairie.add_book, name="addbook"),
    path('al/', librairie.add_librairie, name="add_librairie"),
    path('sl/<int:id>', librairie.show_librairie, name="show_librairie"),
    path('booked/', librairie.show_commandes, name="commandes_livres"),
    
    path('add_order/', librairie.api_add_order, name="api_add_order"),
]

urlpatterns += [ 
    path('alm', marche.listmarkets, name="listmarches"),
   
]