 
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
    path('spages/<int:id>', famille.page_famille, name="page_famille"),
    path('adpa/<int:id>', famille.add_page, name="add_page"),
    path('edf/<int:pk>', famille.edit_famille, name="edit_famille"),
    path('nf/', famille.add_famille, name="add_famille"),
    path('sh_ad_fa/<int:id>', famille.show_admin_fam, name="show_admin_fam"),
    path('add_ad_fam', famille.add_admin_fam, name="add_admin_fam"),
    path("fam/<int:famille_id>", famille.famille_generations, name="famille_generations"),
    path("fam/<int:famille_id>/arbre", famille.famille_arbre, name="famille_arbre"),
    path("fam/<int:famille_id>/ag", famille.famille_arbre_graphique, name="famille_arbre_graphique"),

    path("ev/<int:id>/like", evenement.toggle_like_evenement, name="toggle_like_evenement"),
    path("ev/likes", evenement.mes_evenements_likes, name="mes_evenements_likes"),
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
    path('a/faq', core.faq, name="faq_archcore"),
    path('faqi', core.faqindex, name="faq_index"),
    path('cont', core.contact, name="contact"),

    path('com/<int:community_id>/messages', core.community_messages, name='community_messages'),
    path('com/mess/create', core.create_community_message, name='create_community_message'),
    path('lib/<int:library_id>/messages/', core.library_messages, name='library_messages'),
    path('lib/mess/create', core.create_library_message, name='create_library_message'),
    # path('lib/<int:library_id>/mess/create', core.create_library_message, name='create_library_message'),
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
    path('ec/<int:id>', communaute.edit_communaute, name="edit_communaute"),
    path('na/', communaute.add_association, name="add_association"),
    path('lass/<int:id>.<int:mode>', communaute.listassociations, name="listassociations"),
    path('lassfam/<int:id>', communaute.listassociationsfam, name="listassociationsfam"),
    path('ngal/', communaute.add_galerie, name="add_galerie"),
    path('upim/', communaute.upload_image, name="upload_image"),
    path('ga/<int:id>', communaute.show_galerie, name="show_galerie"),
    path('c/faq', communaute.faq, name="faq_communaute"),

    path('com/<int:community_id>/his', communaute.community_history, name='com_histoire'),
    path('com/<int:community_id>/geo', communaute.community_geography, name='com_geographie'),
    path('com/<int:community_id>/king/<int:king_id>/', communaute.king_detail, name='king_detail'),
    path('com/<int:community_id>/kings', communaute.kings_list, name='kings_list'),

    # Liste des dons d'une communauté
    path('com/<int:communaute_id>/dons',  communaute.don_list, name='don_list'),    
    path('com/<int:communaute_id>/dons/no',  communaute.don_create, name='don_create'),    
    path('com/<int:communaute_id>/dons/<int:don_id>', communaute.don_detail,  name='don_detail'), 
    path('com/<int:communaute_id>/dons/<int:don_id>/mod', communaute.don_update,  name='don_update'),    
    path('com/<int:communaute_id>/dons/<int:don_id>/sup', communaute.don_delete,   name='don_delete'),

    path('com/<int:communaute_id>/pc/ad', communaute.personnecle_create, name='personnecle_create_com'),
    path('fam/<int:famille_id>/pc/ad', communaute.personnecle_create, name='personnecle_create_fam'),

    path('com/<int:communaute_id>/lc/ad', communaute.lieucles_create, name='lieucles_create_com'),
    path('fam/<int:famille_id>/lc/ad', communaute.lieucles_create, name='lieucles_create_fam'),
    path('pe/<int:pk>/sh', communaute.personnecle_detail, name='personnecle_detail'),
    path('pe/<int:pk>/ed', communaute.personnecle_edit, name='personnecle_edit'),

    path('lc/<int:pk>/sh', communaute.lieucle_detail, name='lieucle_detail'),
    path('lc/<int:pk>/ed', communaute.lieucle_edit, name='lieucle_edit'),
    path('lc/<int:pk>/', communaute.lieucle_delete, name='lieucle_delete'),

    path('lcc/<int:idcom>/', communaute.lieucle_create, name='lieucle_create'),
    path('pcc/<int:idcom>/', communaute.personnecle_create, name='personnecle_create'),

    path('pc/<int:pk>/de', communaute.personnecle_delete, name='personnecle_delete'),

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
    path('u/abo', membre.user_abonnement, name="home_abonnement"),    
]

urlpatterns += [ 
    path('libs', librairie.listlibs, name="listlibs"),
    path('libab', librairie.abonement_librairie, name="abonement_librairie"),
    path('lbs/<int:id>.<int:mode>', librairie.listbooks,  name="listbooks"),
    path('sb/<int:id>', librairie.show_book, name="show_book"),
    path('edli/<int:id>', librairie.edit_librairie, name="edit_librairie"),
    path('edb/<int:id>', librairie.edit_book, name="edit_book"),
    path('searb', librairie.search_book, name="search_book"),
    path('searbl/<int:id>', librairie.search_book_lib, name="search_book_lib"),
    path('sbf/<int:id>', librairie.show_book_file, name="show_book_file"),
    path('ab/', librairie.add_book, name="addbook"),
    path('al/', librairie.add_librairie, name="add_librairie"),
    path('sl/<int:id>', librairie.show_librairie, name="show_librairie"),
    path('booked/', librairie.show_commandes, name="commandes_livres"),
    path('faq', librairie.faq, name="faq_librairie"),
    
    path('add_order/', librairie.api_add_order, name="api_add_order"),
    path("liv/<int:livre_id>/pay/", librairie.payer_livre, name="payer_livre"),
    path("liv/<int:paiement_id>/remb/", librairie.rembourser_paiement, name="rembourser_paiement"),
    path("liv/his/", librairie.historique_paiements, name="historique_paiements"),
    path("liv/<int:paiement_id>/pdf/", librairie.facture_pdf, name="facture_pdf"),
    path("fac/verif/<int:reference>", librairie.verifier_facture, name="verifier_facture"),
    
    path("liv/<int:livre_id>/note/", librairie.noter_livre, name="noter_livre"),


]

urlpatterns += [ 
    path('alm', marche.listmarkets, name="listmarches"),
   
]