 
from django.urls import path
import arch_portal.use_cases.marche_controller as marche
import arch_portal.use_cases.librairie_controller as librairie
import arch_portal.use_cases.membre_controller as membre
import arch_portal.use_cases.communaute_controller as communaute
import arch_portal.use_cases.famille_controller as famille
import arch_portal.use_cases.core_controller as core
import arch_portal.use_cases.evenement_controller as evenement

urlpatterns = [ 
    path('lfam/<int:id>.<int:mode>', famille.listfamilles, name="listfamilles"),
    path('sf/<int:id>', famille.show_famille, name="show_famille"),
    path('nf/', famille.add_famille, name="add_famille"),
    path('sh_ad_fa/<int:id>', famille.show_admin_fam, name="show_admin_fam"),
    path('add_ad_fam', famille.add_admin_fam, name="add_admin_fam"),
    path('levts/<int:id>.<int:mode>', evenement.listevenements, name="listevenements"),
    path('sev/<int:id>', evenement.show_evenement, name="show_evenement"),
    path('nev/', evenement.add_evenement, name="add_evenement"),
]

urlpatterns += [ 
    path('', core.index, name="index"),
    path('add_ad_famsalleatt', core.add_user_salleattfam, name="ad_sal_fam"),
    path('add_ad_comsalleatt', core.add_user_salleattcom, name="ad_sal_com"),
    path('add_ad_assosalleatt', core.add_user_salleattasso, name="ad_sal_asso"),
    path('valsatt', core.valide_salleatt, name="valide_salle_att"),
    path('shfasal/<int:id>', core.show_fam_salle, name="show_fam_salle"),
    path('shcosal/<int:id>', core.show_com_salle, name="show_com_salle"),
    path('shassosal/<int:id>', core.show_asso_salle, name="show_asso_salle"),
]
urlpatterns += [ 
    path('lcom', communaute.listcom, name="listcom"),
    path('sh_ad_co/<int:id>', communaute.show_admin_com, name="show_admin_com"),
    path('sh_ad_asso/<int:id>', communaute.show_admin_asso, name="show_admin_asso"),
    path('comab', communaute.abonement_archive, name="abonement_archive"),
    path('add_ad_com', communaute.add_admin_com, name="add_admin_com"),
    path('add_ad_asso', communaute.add_admin_asso, name="add_admin_asso"),
    path('add_abonnement', communaute.add_abonnement, name="add_abonnement"),
    path('sa/<int:id>', communaute.show_association, name="show_association"),
    path('sma/<int:id>', communaute.listmembresassociation, name="listmembresassociation"),
    path('sc/<int:id>', communaute.show_communaute, name="show_communaute"),
    path('nc/', communaute.add_communaute, name="add_communaute"),
    path('na/', communaute.add_association, name="add_association"),
    path('lass/<int:id>.<int:mode>', communaute.listassociations, name="listassociations"),
    path('lassfam/<int:id>', communaute.listassociationsfam, name="listassociationsfam"),
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
    path('u/adfam', membre.show_user_famadmin, name="home_famadmin"),
    path('u/adcom', membre.show_user_comadmin, name="home_comadmin"),
    path('u/adasso', membre.show_user_assoadmin, name="home_assoadmin"),
    path('u/seemes', membre.show_user_messages, name="home_messageadmin"),
    
]

urlpatterns += [ 
    path('libs', librairie.listlibs, name="listlibs"),
    path('libab', librairie.abonement_librairie, name="abonement_librairie"),
    path('lbs/<int:id>.<int:mode>', librairie.listbooks,  name="listbooks"),
    path('sb/<int:id>', librairie.show_book, name="show_book"),
    path('sbf/<int:id>', librairie.show_book_file, name="show_book_file"),
    path('ab/', librairie.add_book, name="addbook"),
    path('al/', librairie.add_librairie, name="add_librairie"),
    path('sl/<int:id>', librairie.show_librairie, name="show_librairie"),
    path('booked/', librairie.show_commandes, name="commandes_livres"),
    
    path('add_order/', librairie.api_add_order, name="api_add_order"),
]

urlpatterns += [ 
    path('alm', marche.listmarkets, name="listmarches"),
   
]