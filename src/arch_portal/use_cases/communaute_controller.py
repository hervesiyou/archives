from django.contrib  import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.conf import settings
# from arch_portal.domain.models import communaute
from arch_portal.domain.forms.don import DonForm
from arch_portal.domain.forms.galerie import GalerieForm
from arch_portal.domain.forms.association import AssociationForm
from arch_portal.domain.forms.communaute import CommunauteForm 
from arch_portal.domain.models.communaute import Communaute
from arch_portal.domain.models.famille import Famille
from arch_portal.domain.models.abonnement import Abonnement
from arch_portal.domain.models.plantarifaire import Plan
from arch_portal.domain.models.roi import Rois
from arch_portal.domain.models import *
from django.contrib.auth.decorators import login_required , permission_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseForbidden, JsonResponse
from arch_portal.domain.models import Association
from django.views.decorators.http import require_http_methods
from django.db import models
from django.forms import inlineformset_factory

from arch_portal.domain.forms.sets import MiniHistoireFormSet, RoiFormSet   

import json
from datetime import date

from arch_portal.domain.models.don import Don
from arch_portal.domain.models.communaute import Communaute   
from arch_portal.domain.models.personnecle import PersonneCle   
from arch_portal.domain.models.lieucle   import LieuCle  
from arch_portal.domain.forms.lieucle   import LieuCleForm  
from arch_portal.domain.forms.personnecle   import PersonneCleForm 


# ────────────── PERSONNES CLÉS ──────────────

 
def personnecle_create(request, type_entite, entite_id):
    """Créer une personne clé pour une Communauté ou une Famille"""

    if type_entite == 'communaute':
        entite = get_object_or_404(Communaute, pk=entite_id)
        redirect_url = entite.get_absolute_url()

    elif type_entite == 'famille':
        entite = get_object_or_404(Famille, pk=entite_id)
        redirect_url = entite.get_absolute_url()
    else:
        messages.error(request, "Type d'entité invalide.")
        return redirect('home')

    if request.method == 'POST':
        form = PersonneCleForm(request.POST, request.FILES)
        if form.is_valid():
            personne = form.save()
            if type_entite == 'communaute':
                personne.communautes.add(entite)
            else:
                personne.familles.add(entite)

            messages.success(request, f"{personne.nom} ajouté(e) comme personne clé.")
            return redirect(redirect_url)
    else:
        form = PersonneCleForm()

    return render(request, 'archcore/creepersonnecle.html', {
        'form': form,
        'titre': f"Ajouter une personne clé à {entite}",
        'soustitre': entite.nom,
        'bouton': "Ajouter",
        'back_url': redirect_url,
    })

def lieucles_create(request, type_entite, entite_id):

    if type_entite == 'communaute':
        entite = get_object_or_404(Communaute, pk=entite_id)
        redirect_url = entite.get_absolute_url()
    elif type_entite == 'famille':
        entite = get_object_or_404(Famille, pk=entite_id)
        redirect_url = entite.get_absolute_url()
    else:
        messages.error(request, "Type d'entité invalide.")
        return redirect('home')

    if request.method == 'POST':
        form = LieuCleForm(request.POST, request.FILES)
        if form.is_valid():
            lieu = form.save()
            if type_entite == 'communaute':
                lieu.communautes.add(entite)
            else:
                lieu.familles.add(entite)

            messages.success(request, f"{lieu.nom} ajouté comme lieu clé.")
            return redirect(redirect_url)
    else:
        form = LieuCleForm()

    return render(request, 'archcore/creelieucle.html', {
        'form': form,
        'titre': f"Ajouter un lieu clé à {entite}",
        'soustitre': entite.nom,
        'bouton': "Ajouter",
        'back_url': redirect_url,
    })


def personnecle_detail(request, pk):
    personne = get_object_or_404(PersonneCle, pk=pk)
    # Vérifier droits d'accès si besoin (ex: si liée à communauté/famille privée)
    return render(request, 'archcore/personnecle_detail.html', {
        'personne': personne,
        'titre': f"Détails de {personne.nom}",
    })
 
def personnecle_edit(request, pk):
    personne = get_object_or_404(PersonneCle, pk=pk)
    
    if request.method == 'POST':
        form = PersonneCleForm(request.POST, request.FILES, instance=personne)
        if form.is_valid():
            form.save()
            messages.success(request, f"{personne.nom} a été modifié avec succès.")
            return redirect('personnecle_detail', pk=personne.pk)
    else:
        form = PersonneCleForm(instance=personne)

    return render(request, 'archore/creepersonnecle.html', {
        'form': form,
        'titre': f"Modifier {personne.nom}",
        'bouton': "Mettre à jour",
        'back_url': personne.get_absolute_url(),
    })


# ────────────── LIEU CLÉ ──────────────
 
def lieucle_detail(request, pk):
    lieu = get_object_or_404(LieuCle, pk=pk)
    return render(request, 'archcore/lieucle_detail.html', {
        'lieu': lieu,
        'titre': f"Détails de {lieu.nom}",
    })

 
def lieucle_edit(request, pk):
    lieu = get_object_or_404(LieuCle, pk=pk)
    
    if request.method == 'POST':
        form = LieuCleForm(request.POST, request.FILES, instance=lieu)
        if form.is_valid():
            form.save()
            messages.success(request, f"{lieu.nom} a été modifié avec succès.")
            return redirect('lieucle_detail', pk=lieu.pk)
    else:
        form = LieuCleForm(instance=lieu)

    return render(request, 'archcore/creelieucle.html', {
        'form': form,
        'titre': f"Modifier {lieu.nom}",
        'bouton': "Mettre à jour",
        'back_url': lieu.get_absolute_url(),
    })

 
def personnecle_delete(request, pk):
    personne = get_object_or_404(PersonneCle, pk=pk)
    personne.delete()
    messages.success(request, "Personne clé supprimée.")
    return redirect('home')  # ou vers la liste

 
def lieucle_delete(request, pk):
    lieu = get_object_or_404(LieuCle, pk=pk)
    lieu.delete()
    messages.success(request, "Lieu clé supprimée.")
    return redirect('home')  # ou vers la liste

# @login_required
def don_list(request, communaute_id):
    
    communaute = get_object_or_404(Communaute, id=communaute_id)
    dons = Don.objects.filter(communaute=communaute).order_by('-date_don')
    
    context = {
        'communaute': communaute,
        'dons': dons,
    }
    return render(request, 'archcore/don_list.html', context)


# @login_required
def don_create(request, communaute_id):
    communaute = get_object_or_404(Communaute, id=communaute_id)
    
    if request.method == 'POST':

        userid = request.session.get("userid","")
        user = Membre.objects.get(id=userid)
        if user != None:

            form = DonForm(request.POST)
            if form.is_valid():
                don = form.save(commit=False)
                don.communaute = communaute
                don.donateur = user 
                don.save()
                messages.success(request, "Votre don a été enregistré. Merci beaucoup ! 🙏")
                return redirect('don_list', communaute_id=communaute.id)
        else:
            return redirect("login")
        
    else:
        form = DonForm()
    
    context = {
        'form': form,
        'communaute': communaute,
        'titre': f"Faire un don à {communaute.nom}"
    }
    return render(request, 'archcore/don_form.html', context)


# @login_required
def don_detail(request, communaute_id, don_id):
    communaute = get_object_or_404(Communaute, id=communaute_id)
    don = get_object_or_404(Don, id=don_id, communaute=communaute)
    
    context = {
        'don': don,
        'communaute': communaute,
    }
    return render(request, 'archcore/don_detail.html', context)


# @login_required
def don_update(request, communaute_id, don_id):
    communaute = get_object_or_404(Communaute, id=communaute_id)
    don = get_object_or_404(Don, id=don_id, communaute=communaute)
    
    userid = request.session.get("userid","")
    user = Membre.objects.get(id=userid)
    if user != None:
        # Autorisation : donateur ou admin de la communauté
        if don.donateur != user and user not in communaute.administrateurs.all():
            return HttpResponseForbidden("Vous n'êtes pas autorisé à modifier ce don.")
    else:
            return redirect("login")
    
    if request.method == 'POST':
        form = DonForm(request.POST, instance=don)
        if form.is_valid():
            form.save()
            messages.success(request, "Le don a été modifié avec succès.")
            return redirect('don_detail', communaute_id=communaute.id, don_id=don.id)
    else:
        form = DonForm(instance=don)
    
    context = {
        'form': form,
        'communaute': communaute,
        'don': don,
        'titre': "Modifier le don"
    }
    return render(request, 'archcore/don_form.html', context)


# @login_required
def don_delete(request, communaute_id, don_id):
    communaute = get_object_or_404(Communaute, id=communaute_id)
    don = get_object_or_404(Don, id=don_id, communaute=communaute)
    
    userid = request.session.get("userid","")
    user = Membre.objects.get(id=userid)
    if user != None:
        # Même règle d'autorisation
        if don.donateur != user and user not in communaute.administrateurs.all():
            return HttpResponseForbidden("Vous n'êtes pas autorisé à supprimer ce don.")
    else:
            return redirect("login")
    
    if request.method == 'POST':
        don.delete()
        messages.warning(request, "Le don a été supprimé.")
        return redirect('don_list', communaute_id=communaute.id)
    
    context = {
        'don': don,
        'communaute': communaute,
    }
    return render(request, 'archcore/don_delete.html', context)


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

    return render(request, "archcore/show_com.html", 
        {
            "communaute":com, 
            "appartient" : appartient,
            'personnes_cles': com.personnes_cles.all().order_by('nom'),
            'lieux_cles': com.lieux_cles.all().order_by('nom'),
        }
    )

def show_admin_com(request,id):
    com = Communaute.objects.get(id=id)
    # print(com.administrateurs.all())
    return render(request, "archcore/listadmincom.html", {"admins": com.administrateurs.all(), "communaute": com})

def show_admin_asso(request,id):
    com = Association.objects.get(id=id)
    # print(com.administrateurs.all())
    return render(request, "archcore/listadminasso.html", {"admins": com.administrateurs.all(), "association": com})

def edit_communaute(request, id):
    com = get_object_or_404(Communaute, id=id)
    if request.method == "POST":
        form = CommunauteForm(request.POST, instance=com) 
        histoires_formset = MiniHistoireFormSet(request.POST, instance=com, prefix='mini_histoire')
        rois_formset = RoiFormSet(request.POST, instance=com, prefix='rois_communaute')

        if form.is_valid() and histoires_formset.is_valid() and rois_formset.is_valid():  
            com = form.save() 
            com.save()
            histoires_formset.save()
            rois_formset.save()
            messages.success(request, "Communauté modifiée avec succès.")
            return redirect("show_communaute",com.id )
    else:
        form = CommunauteForm(instance=com)
        histoires_formset =MiniHistoireFormSet(instance=com, prefix='mini_histoire')
        rois_formset = RoiFormSet(instance=com, prefix='rois_communaute')

    context ={
        "form": form,
        "histoires_formset": histoires_formset,
        "rois_formset": rois_formset,
        "titre": f"Modification - {com.nom}",
        "action": "Modifier",
        "communaute": com
    }

    return render(request, "archcore/new_communaute.html",  context )

def add_communaute(request):

    PersonneFormSet = inlineformset_factory(
        Communaute, PersonneCle, form=PersonneCleForm,
        fields='__all__', extra=1, can_delete=True
    )
    LieuFormSet = inlineformset_factory(
        Communaute, LieuCle, form=LieuCleForm,
        fields='__all__', extra=1, can_delete=True
    )
    
    if request.method == "POST":
        form = CommunauteForm(request.POST)

        histoires_formset = MiniHistoireFormSet(request.POST, instance=Communaute())
        rois_formset = RoiFormSet(request.POST, instance=Communaute())

        personnes_formset = PersonneFormSet(request.POST, instance=Communaute(), prefix='personnes')
        lieux_formset = LieuFormSet(request.POST, instance=Communaute(), prefix='lieux')
        
        if form.is_valid() and histoires_formset.is_valid() and rois_formset.is_valid():  
            com = form.save() 
            com.save()

            histoires_formset.instance = com
            histoires_formset.save()

            rois_formset.instance = com
            rois_formset.save()

            personnes_formset.instance = com
            personnes_formset.save()

            lieux_formset.instance = com
            lieux_formset.save()

            messages.success(request, "Communauté créée avec succès.")
            
            return redirect("show_communaute",com.id )
        else:
            messages.error(request, "Erreur lors de la création de la communauté. Veuillez vérifier les informations saisies.")
    else:
        form = CommunauteForm()
        form = CommunauteForm()
        histoires_formset = MiniHistoireFormSet(instance=Communaute())
        rois_formset = RoiFormSet(instance=Communaute())
        

        personnes_formset = PersonneFormSet(instance=Communaute(), prefix='personnes')
        lieux_formset = LieuFormSet(instance=Communaute(), prefix='lieux')

    context = {
        'form': form,
        'histoires_formset': histoires_formset,
        'rois_formset': rois_formset,

        'personnes_formset': personnes_formset,
        'lieux_formset': lieux_formset,
        
        'titre': "Créer une nouvelle communauté",
        'action': "Créer",
    }

    return render(request, "archcore/new_communaute.html", context)

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
    com = Communaute.objects.get(id=community_id)
    # histoires = com.histoires.all().order_by('-date', 'nom')
    
    histoires = com.histoires.filter(
        models.Q(nom__isnull=False) & ~models.Q(nom="") |
        models.Q(description__isnull=False) & ~models.Q(description="")
    ).order_by('-date', 'nom')

    context = {
        'community_id': community_id,
        'community_name': com.nom,
        "histoires":  histoires,
        'history': {
            'origin': com.origine,
            'chief': com.chef.nomcomplet if com.chef else "Inconnu",
            'description': com.histoire,
            # 'key_events': [
            #     {'year': 1950, 'event': 'Fondation de la communauté'},
            #     {'year': 1975, 'event': 'Premier grand rassemblement'},
            #     {'year': 2000, 'event': 'Modernisation des structures'},
            #     {'year': 2020, 'event': 'Intégration numérique'},
            # ]
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
        'geographie': community.geographie,
        # 'latitude': 6.8276, 
        # 'longitude': -0.7893,
        'map_zoom': 12,
        # 'geography': {
        #     'region': 'Région --',
        #     'country': 'Pays --',
        #     'area_km2': 1500,
        #     'population': 250000,
        #     'climate': 'Tropical',
        #     'terrain': 'Accidenté avec vallées'
        # }
    }
    return render(request, 'archcore/com_geo.html', context)

# Afficher les informations détaillées sur un roi
@require_http_methods(["GET"])
def king_detail(request, community_id, king_id):
    community = Communaute.objects.get(id=community_id)
    roi = Rois.objects.get(id=king_id)

    context = {
        'community_id': community_id,
        'community_name': f"{community.nom}",
        "roi": roi ,

        # 'king': {
        #     'id': king_id,
        #     'name': 'Roi ',
        #     'reign_start': 1985,
        #     'reign_end': 2010,
        #     'biography': 'Biographie détaillée du roi...',
        #     'achievements': [
        #         'Réforme administrative',
        #         'Expansion territoriale',
        #         'Développement des arts',
        #     ],
        #     'family': {
        #         'father': 'Père  ',
        #         'mother': 'Mère  ',
        #         'successors': 'Successeur  '
        #     }
        # }
    }
    return render(request, 'archcore/king_detail.html', context)

# Afficher la liste des rois d'une communauté
@require_http_methods(["GET"])
def kings_list(request, community_id):
    community = Communaute.objects.get(id=community_id)
    context = {
        'community_id': community_id,
        'communaute': community,
        'rois': community.rois.all(),
        'community_name': f'{community.nom}',
        'description': f'{community.description}',
        # 'kings': [
        #     {
        #         'id': 1,
        #         'name': 'Roi   1',
        #         'reign_period': '1950-1975',
        #         'photo': '/static/images/rois.jpg',
        #         'status': 'Décédé'
        #     },
        #     {
        #         'id': 2,
        #         'name': 'Roi   2',
        #         'reign_period': '1975-2000',
        #         'photo': '/static/images/king2.jpg',
        #         'status': 'Décédé'
        #     },
        #     {
        #         'id': 3,
        #         'name': 'Roi   3',
        #         'reign_period': '2000-Présent',
        #         'photo': '/static/images/king3.jpg',
        #         'status': 'En vie'
        #     },
        # ]
    }
    return render(request, 'archcore/king_list.html', context)
