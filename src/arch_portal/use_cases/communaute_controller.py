from django.shortcuts import redirect, render
from django.conf import settings
from arch_portal.domain.forms.galerie import GalerieForm
from arch_portal.domain.forms.association import AssociationForm
from arch_portal.domain.forms.communaute import CommunauteForm 
from arch_portal.domain.models.communaute import Communaute
from arch_portal.domain.models.famille import Famille
from arch_portal.domain.models.abonnement import Abonnement
from arch_portal.domain.models.plantarifaire import Plan
from arch_portal.domain.models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseForbidden, JsonResponse
from arch_portal.domain.models import Association
from django.views.decorators.http import require_http_methods

import json
from datetime import date

@login_required
def premium_content(request):
    user = request.user
    if not hasattr(user, 'subscription') or not user.subscription.is_active:
        return HttpResponseForbidden("Vous devez être abonné pour accéder à ce contenu.")
    return render(request, 'premium_content.html')

# @login_required
@csrf_exempt
def add_abonnement(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax :
        if request.method == "POST" :
            data = json.loads(request.body.decode('utf-8'))
            userid = request.session.get("userid","")
            # user = f' un: {request.session.get("username","")} ,id: {request.session.get("userid","")},n: {request.session.get("nomocomplet","")}'
            # print(data ,data.get("code"))
            
            if data.get('nbannee') is None:
                return JsonResponse({'status': False ,"message": "Nombre d'année incorrect"})
            else:
                if data.get("code") is None:
                    return JsonResponse({'status': False ,"message": "Identification abonnement incorrecte"})
                else:
                    if userid is None:
                        return JsonResponse({'status': False ,"message": "Merci de vous connecter avant tout abonnement !"})
                    else:
                        user = Membre.objects.get(id=userid)
                        plan = Plan.objects.get(code=data.get("code"))
                        

                        ab = Abonnement.objects.filter(plan=plan, membre=user)
                        # print(ab, plan, user)
                        if len(ab) == 0:
                            #  je lui ajoute le role client
                            role = Role.objects.get(nom="CLIENT")
                            user.role.add(role)
                            ab = Abonnement(
                                code= f"{plan.code}@{plan.appli}",
                                debut= date.today(),
                                prix= int(data.get("nbannee")) * plan.prix,
                                membre= user,
                                plan= plan,
                                duree = int(data.get("nbannee"))
                            )
                            ab.save()
                            user.save()
                            message = f'''Merci de faire le depot au numero {settings.NO_ORANGE} pour OM et  {settings.NO_MTN} pour MOMO pour l'activation de votre compte !
                            '''
                            return JsonResponse({'status': True ,"message": message})
                        else:
                            return JsonResponse({'status': False ,"message": "Desolé, vous avez dejà souscris à cet abonnement !"})


@csrf_exempt
def add_admin_com(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax :
        if request.method == "POST" :
            data = json.loads(request.body.decode('utf-8'))
            userid = request.session.get("userid","")
            # user = f' un: {request.session.get("username","")} ,id: {request.session.get("userid","")},n: {request.session.get("nomocomplet","")}'
             
            if data.get('comid') is None:
                return JsonResponse({'status': False ,"message": "Communauté incorrecte !"})
            else:
                if data.get("adminid") is None:
                    return JsonResponse({'status': False ,"message": "Identification utilisateur incorrecte"})
                else:
                    if userid is None:
                        return JsonResponse({'status': False ,"message": "Merci de vous connecter avant tout abonnement !"})
                    else:
                        user = Membre.objects.get(id=data.get("adminid"))
                        com = Communaute.objects.get(id=data.get("comid"))
                        role = Role.objects.get(nom="ADMIN")
                        # print(role, user)
                        user.role.add(role)
                        user.save()
                        com.administrateurs.add(user)
                        com.save()

                        
                        return JsonResponse({'status': True ,"message": f"{user.nomcomplet} a été ajouté comme administrateur à la communauté {com.nom}"})

@csrf_exempt
def add_admin_asso(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax :
        if request.method == "POST" :
            data = json.loads(request.body.decode('utf-8'))
            userid = request.session.get("userid","")
            # user = f' un: {request.session.get("username","")} ,id: {request.session.get("userid","")},n: {request.session.get("nomocomplet","")}'
             
            if data.get('assoid') is None:
                return JsonResponse({'status': False ,"message": "Association incorrecte !"})
            else:
                if data.get("adminid") is None:
                    return JsonResponse({'status': False ,"message": "Identification utilisateur incorrecte"})
                else:
                    if userid is None:
                        return JsonResponse({'status': False ,"message": "Merci de vous connecter avant tout abonnement !"})
                    else:
                        user = Membre.objects.get(id=data.get("adminid"))
                        asso = Association.objects.get(id=data.get("assoid"))
                        role = Role.objects.get(nom="ADMIN")
                        # print(role, user)
                        user.role.add(role)
                        user.save()
                        asso.administrateurs.add(user)
                        asso.save()

                        
                        return JsonResponse({'status': True ,"message": f"{user.nomcomplet} a été ajouté comme administrateur à l'association {asso.nom}"})
                      

def abonement_archive(request): 
    plans = Plan.objects.filter(appli="COM")
    return render(request, "archcore/abonement.html", {"plans" : plans} )

def faq(request): 
    # plans = Plan.objects.filter(appli="COM")
    return render(request, "archcore/faqcom.html", {} )

def listcom(request):
    communautes = Communaute.objects.all()
    return render(request, "archcore/listcom.html", { "communautes":communautes, })
 
def show_association(request,id):
    asso = Association.objects.get(id=id)
    return render(request, "archcore/showassociation.html", {"association": asso})

def listassociationsfam(request, id): 
    com = Famille.objects.get(id=id)
    return render(request, "archcore/listassociationsfam.html", { "famille": com})

def listmembresassociation(request, id): 
    com = Association.objects.get(id=id)
    return render(request, "archcore/listmembresassociation.html", { "association": com})


def listassociations(request, id, mode = 0):
    assos = Association.objects.filter(communaute=id)
    com = Communaute.objects.get(id=id)
    if not mode:
        return render(request, "archcore/listassociations_tab.html", {"associations": assos, "communaute": com})
    return render(request, "archcore/listassociations.html", {"associations": assos, "communaute": com})

def add_association(request):
    if request.method == "POST":
        form = AssociationForm(request.POST)
        if form.is_valid():  
            com = form.save() 
            com.save()
            
            return redirect("show_association", com.id )
    else:
        form = AssociationForm()

    return render(request, "archcore/new_association.html", { "form":form  })
 

def show_communaute(request, id):
    com = Communaute.objects.get(id=id)
    #  ce utilisateur ne peut voir les info detaillée de la famille que si il appartient à la famille ou a des droits
    userid = request.session.get("userid","")
    if not userid :
        # print(f" user id { userid } ")
        return redirect("login" )

    user = Membre.objects.get(id=userid)
    appartient=False
    if ( user in com.membres_communaute.all()):
        appartient = True

    return render(request, "archcore/show_com.html", {"communaute":com, "appartient" : appartient})

def show_admin_com(request,id):
    com = Communaute.objects.get(id=id)
    # print(com.administrateurs.all())
    return render(request, "archcore/listadmincom.html", {"admins": com.administrateurs.all(), "communaute": com})

def show_admin_asso(request,id):
    com = Association.objects.get(id=id)
    # print(com.administrateurs.all())
    return render(request, "archcore/listadminasso.html", {"admins": com.administrateurs.all(), "association": com})

def add_communaute(request):
    
    if request.method == "POST":
        form = CommunauteForm(request.POST)
        if form.is_valid():  
            com = form.save() 
            com.save()
            return redirect("show_communaute",com.id )
    else:
        form = CommunauteForm()

    return render(request, "archcore/new_communaute.html", { "form":form })

def show_galerie(request, id):
    pass
def add_galerie(request):
    
    if request.method == "POST":
        form = GalerieForm(request.POST)
        if form.is_valid():  
            com = form.save() 
            com.save()
            
            return redirect("show_galerie",com.id )
    else:
        form = GalerieForm()

    return render(request, "usercore/new_galerie.html", { "form":form  })


# Afficher l'histoire d'une communauté
@require_http_methods(["GET"])
def community_history(request, community_id):
    context = {
        'community_id': community_id,
        'community_name': 'Communauté Exemple',
        'history': {
            'founded_year': 1950,
            'founder': 'Fondateur Exemple',
            'description': 'Ceci est l\'histoire détaillée de la communauté...',
            'key_events': [
                {'year': 1950, 'event': 'Fondation de la communauté'},
                {'year': 1975, 'event': 'Premier grand rassemblement'},
                {'year': 2000, 'event': 'Modernisation des structures'},
                {'year': 2020, 'event': 'Intégration numérique'},
            ]
        }
    }
    return render(request, 'archcore/com_histoire.html', context)


# Afficher la géographie d'une communauté avec carte Google Maps
@require_http_methods(["GET"])
def community_geography(request, community_id):
    community = Communaute.objects.get(id=community_id)
    context = {
        'community_id': community_id,
        'community_name': f"{community.nom}",
        'geographie': f"{community.geographie}",
        'latitude': 6.8276,  # Exemple: Accra, Ghana
        'longitude': -0.7893,
        'map_zoom': 12,
        'geography': {
            'region': 'Région --',
            'country': 'Pays --',
            'area_km2': 1500,
            'population': 250000,
            'climate': 'Tropical',
            'terrain': 'Accidenté avec vallées'
        }
    }
    return render(request, 'archcore/com_geo.html', context)


# Afficher les informations détaillées sur un roi
@require_http_methods(["GET"])
def king_detail(request, community_id, king_id):
    community = Communaute.objects.get(id=community_id)
    context = {
        'community_id': community_id,
        'community_name': f"{community.nom}",
        'king': {
            'id': king_id,
            'name': 'Roi Exemple',
            'reign_start': 1985,
            'reign_end': 2010,
            'biography': 'Biographie détaillée du roi...',
            'achievements': [
                'Réforme administrative',
                'Expansion territoriale',
                'Développement des arts',
            ],
            'family': {
                'father': 'Père Exemple',
                'mother': 'Mère Exemple',
                'successors': 'Successeur Exemple'
            }
        }
    }
    return render(request, 'archcore/king_detail.html', context)


# Afficher la liste des rois d'une communauté
@require_http_methods(["GET"])
def kings_list(request, community_id):
    community = Communaute.objects.get(id=community_id)
    context = {
        'community_id': community_id,
        'communaute': community,
        'community_name': f'{community.nom}',
        'kings': [
            {
                'id': 1,
                'name': 'Roi Exemple 1',
                'reign_period': '1950-1975',
                'photo': '/static/images/king1.jpg',
                'status': 'Décédé'
            },
            {
                'id': 2,
                'name': 'Roi Exemple 2',
                'reign_period': '1975-2000',
                'photo': '/static/images/king2.jpg',
                'status': 'Décédé'
            },
            {
                'id': 3,
                'name': 'Roi Exemple 3',
                'reign_period': '2000-Présent',
                'photo': '/static/images/king3.jpg',
                'status': 'En vie'
            },
        ]
    }
    return render(request, 'archcore/king_list.html', context)
