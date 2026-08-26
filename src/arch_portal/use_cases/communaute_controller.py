 
 
from arch_portal.use_cases.services.core import update_member_badges
from arch_portal.domain.models.galerie import Galerie
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
from arch_portal.domain.forms.image import ImageForm
from arch_portal.domain.models.abonnement import Abonnement
from arch_portal.domain.models.plantarifaire import Plan
from arch_portal.domain.models.roi import Rois
from arch_portal.domain.models.image import Image
from django.http import HttpResponseForbidden, JsonResponse

from arch_portal.domain.models.histoire import MiniHistoire
from arch_portal.domain.models import *
from django.contrib.auth.decorators import login_required , permission_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from arch_portal.domain.models import Association
from django.views.decorators.http import require_http_methods
# from django.db import models
from django.forms import inlineformset_factory
from arch_portal.domain.forms.sets import MiniHistoireFormSet, RoiFormSet , RoiForm, MiniHistoireForm
from django.urls import reverse 
from django.core.exceptions import PermissionDenied
from arch_portal.use_cases.services.subscription_service import check_abonnement_permission, get_membre_from_session

import json
from datetime import date

from arch_portal.domain.models.don import Don
# from arch_portal.domain.models.communaute import Communaute   
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
    
    userid = request.session.get("userid","")
    user = Membre.objects.get(id=userid)
    
    if request.method == 'POST':        
        if user != None:

            form = DonForm(request.POST)
            if form.is_valid():
                don = form.save(commit=False)
                don.communaute = communaute
                don.donateur = user 
                don.save()
                messages.success(request, "Votre don a été enregistré. Merci beaucoup ! 🙏")

                 # je met a jour le badge du membre
                update_member_badges(user)

                return redirect('don_list', communaute_id=communaute.id)
        else:
            # return redirect("login")
            return redirect(f"{reverse('login')}?next={request.get_full_path()}")
        
    else:
        form = DonForm()
    
        context = {
            'form': form,
            'communaute': communaute,
            'titre': f"Faire un don à {communaute.nom}",
            'user': user
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
            return redirect(f"{reverse('login')}?next={request.get_full_path()}")
    
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
            return redirect(f"{reverse('login')}?next={request.get_full_path()}")
    
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
                            message = f'''Merci de faire le depot au numero {settings.NO_ORANGE} pour OM et  {settings.NO_MTN} pour MOMO pour l'activation de votre compte ! '''
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
    galerie = Galerie.objects.filter(association=asso)
    return render(request, "archcore/showassociation.html", {"association": asso, "galerie": galerie})

def edit_association(request,id):
    association= get_object_or_404(Association, pk=id)
    galerie = Galerie.objects.filter(association=association)

    admin = False

    user = request.session['userid']
    user = get_object_or_404(Membre, pk=user)
    if not user:
        messages.error(request, "Merci de vous connecter au prealable.")
        # return redirect("login")
        return redirect(f"{reverse('login')}?next={request.get_full_path()}")
    
    if user in association.administrateurs.all():
        admin = True
       
    if not( association.administrateurs.filter(id=user.id).exists() or ("ADD_ASSOCIATION" in request.session["userrights"] )) :
        messages.error(request, "Vous n'avez pas les droits pour modifier cette association.")
        return redirect('show_association', id=association.id)

    if request.method == 'POST':
        form = AssociationForm(request.POST, instance=association)
        
        if form.is_valid():
            form.save()
            messages.success(request, f"L'association '{association.nom}' a été mise à jour avec succès.")
            return redirect('show_association', id=association.id)
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")

    else:
        form = AssociationForm(instance=association)

    return render(request, "archcore/editassociation.html", {"form":form, "association": association, "galerie": galerie, "admin":admin})

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

    user = get_membre_from_session(request)
    if request.method == "POST":
        try:

            check_abonnement_permission(request, 'association')             
            form = AssociationForm(request.POST)
            
            if form.is_valid(): 
                association = form.save(commit=False)
                association.createur = user
                association.save()

                form.save_m2m()
                # ajouter le créateur comme membre
                user.associations.add(association)
                # ajouter le créateur comme admin
                association.administrateurs.add(user)

                # com = form.save() 
                # com.save()
                
                return redirect("show_association", association.id )
        except PermissionDenied as e:
            form = AssociationForm(user=user)
            messages.error(request, f"Vous n'avez pas les droits nécessaires {str(e)}")
            # return redirect('upgrade_abonnement')  
    
    else:
        # user = request.session['userid']
        # user = get_object_or_404(Membre, pk=user)
        form = AssociationForm(user=user)

    return render(request, "archcore/new_association.html", { "form":form  })
 
def personnecle_create(request, idcom):
    com = Communaute.objects.get(id=idcom)

    if( request.method == "POST" ):
        person_form = PersonneCleForm(request.POST,request.FILES) 

        if (person_form.is_valid()):
            person = person_form.save(commit=False)
            person.communaute = com
            
            person.save()
            com.save()
            messages.success(request, f"{person.nom} ajouté avec success !.")
            
        else:
            messages.error(request, "Informations invalides.")       
     

    return redirect("show_communaute",com.id )

def lieucle_create(request, idcom):
    com = Communaute.objects.get(id=idcom) 

    if( request.method == "POST" ):
        person_form = LieuCleForm(request.POST,request.FILES)
        
        print(request.POST["nom"])
        print(person_form.errors)

        if (person_form.is_valid()):
            person = person_form.save(commit=False)
            person.communaute = com
            
            person.save()
            com.save()
            messages.success(request, f"{person.nom} ajouté avec success !.")
            
        else:
            messages.error(request, "Informations invalides.")       
     

    return redirect("show_communaute",com.id )

def show_communaute(request, id):
    com = Communaute.objects.get(id=id)

    form_personne = PersonneCleForm()
    form_lieu = LieuCleForm()
    #  ce utilisateur ne peut voir les info detaillée de la famille que si il appartient à la famille ou a des droits
    userid = request.session.get("userid","")
    if not userid :
        # print(f" user id { userid } ")
        return redirect(f"{reverse('login')}?next={request.get_full_path()}")
        # return redirect("login" )

    user = Membre.objects.get(id=userid)
    try:
        galerie = Galerie.objects.get(id=com.id)
    except Galerie.DoesNotExist:
        galerie = None
        
    appartient=False
    if ( user in com.membres_communaute.all()):
        appartient = True

    return render(request, "archcore/show_com.html", 
        {
            "communaute":com, 
            "galerie":galerie, 
            "appartient" : appartient,
            'personnes_cles': com.personnescles_communaute.all().order_by('nom'),
            'lieux_cles': com.lieucles_communaute.all().order_by('nom'),

            'form_personne': form_personne,
            'form_lieu': form_lieu
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

@csrf_protect
def edit_communaute(request, id):
    com = get_object_or_404(Communaute, id=id)
    '''
    PersonneFormSet = inlineformset_factory(
        Communaute, PersonneCle, form=PersonneCleForm,
        fields='__all__', extra=1, can_delete=True
    )
    LieuFormSet = inlineformset_factory(
        Communaute, LieuCle, form=LieuCleForm,
        fields='__all__', extra=1, can_delete=True
    )
    '''

    image_instance = com.image if hasattr(com, 'image') else None

    if request.method == "POST":
        form = CommunauteForm(request.POST, instance=com) 
        image_form = ImageForm(request.POST, request.FILES, instance=image_instance)

        histoires_formset = MiniHistoireFormSet(request.POST, instance=com, prefix='mini_histoire')
        rois_formset = RoiFormSet(request.POST, instance=com, prefix='rois_communaute') 
        # personnes_formset = PersonneFormSet(request.POST,request.FILES, instance=com, prefix='personnes')
        # lieux_formset     = LieuFormSet(request.POST, request.FILES, instance=com, prefix='lieux')

        if all( [
            form.is_valid() and 
            histoires_formset.is_valid() and 
            rois_formset.is_valid() and 
            image_form.is_valid()   
            # and
            # personnes_formset.is_valid() 
            # and lieux_formset.is_valid()
        ]) :  
            
            com = form.save(commit=False) 
            com.save()
            histoires_formset.save()
            rois_formset.save()
            
            '''
            personnes_formset.instance = com
            lieux_formset.instance     = com

            personnes = personnes_formset.save(commit=False)
            lieux_formset.save()

            for form in personnes_formset:
                if form.is_valid():  # déjà vérifié globalement, mais safe
                    personne = form.save(commit=False)
                    photo_field = form['photo']  # ou le nom exact du champ file
                    if photo_field.value():      # ou if form.cleaned_data.get('photo')
                        file = request.FILES.get(photo_field.html_name)
                        if file:
                            img = Image.objects.create(
                                fichier=file,
                                titre=f"Photo de {personne.nom or 'personne'}"
                            )
                            personne.photo = img
                    personne.save()
            
            personnes_formset.save()
            '''

            # lieux_formset.save()
            # sauvegarde de l'image de la communauté
            image = image_form.save(commit=False)
            if image_form.cleaned_data.get('fichier'):  # nouveau fichier
                image = image_form.save()
                com.image = image
            elif image_form.cleaned_data.get('DELETE', False):  # si tu ajoutes un champ delete
                com.image = None

            com.save()    
            form.save_m2m()            

            messages.success(request, "Communauté modifiée avec succès.")
            return redirect("show_communaute",com.id )
    else:
        form = CommunauteForm(instance=com)
        histoires_formset = MiniHistoireFormSet(instance=com, prefix='mini_histoire')
        rois_formset = RoiFormSet(instance=com, prefix='rois_communaute')
        # personnes_formset = PersonneFormSet( instance=com, prefix='personnes')
        # lieux_formset     = LieuFormSet( instance=com, prefix='lieux')

        image_form = ImageForm()
   
    context ={
        "form": form,
        "histoires_formset": histoires_formset,
        "rois_formset": rois_formset,

        # 'personnes_formset': personnes_formset,
        # 'lieux_formset': lieux_formset,

        "titre": f"Modification - {com.nom}",
        "action": "Modifier",
        'image_form': image_form,
        "communaute": com
    }

    return render(request, "archcore/new_communaute.html",  context )

def add_communaute(request):
    # Définir les formsets inline (on les crée une seule fois)
    MiniHistoireFormSet = inlineformset_factory(
        Communaute, MiniHistoire, form=MiniHistoireForm,
        fields='__all__', extra=1, can_delete=True
    )
    RoiFormSet = inlineformset_factory(
        Communaute, Rois, form=RoiForm,
        fields='__all__', extra=1, can_delete=True
    )
    PersonneFormSet = inlineformset_factory(
        Communaute, PersonneCle, form=PersonneCleForm,
        fields='__all__', extra=1, can_delete=True
    )
    LieuFormSet = inlineformset_factory(
        Communaute, LieuCle, form=LieuCleForm,
        fields='__all__', extra=1, can_delete=True
    )

    # image_instance = com.image if hasattr(com, 'image') else None   

    if request.method == "POST":

        try:

            check_abonnement_permission(request, 'communaute')
            user = get_membre_from_session(request)
            form = CommunauteForm(request.POST)

            # Créer les formsets avec une instance temporaire vide au début
            histoires_formset = MiniHistoireFormSet(request.POST, instance=Communaute(), prefix='mini_histoire')
            rois_formset      = RoiFormSet(request.POST, instance=Communaute(), prefix='rois_communaute')
            personnes_formset = PersonneFormSet(request.POST, instance=Communaute(), prefix='personnes')
            lieux_formset     = LieuFormSet(request.POST, instance=Communaute(), prefix='lieux')  
            image_form = ImageForm(request.POST, request.FILES)      

            # Validation complète
            if (form.is_valid() and 
                histoires_formset.is_valid() and 
                rois_formset.is_valid() and 
                personnes_formset.is_valid() and 
                lieux_formset.is_valid() and
                image_form.is_valid()
            ) :

                # Sauvegarde principale d'abord → on obtient un ID !
                com = form.save()
                com.createur = user
                # Ré-associer les formsets à l’objet réel sauvegardé
                histoires_formset.instance = com
                rois_formset.instance      = com

                personnes_formset.instance = com
                lieux_formset.instance     = com
                # Sauvegarde des inline maintenant que l’instance parent existe
                histoires_formset.save()
                rois_formset.save()

                # sauvegarde de l'image de la communauté et ajout de l'actuel ccreateur comme administrateur
                membre = get_membre_from_session(request)
                com.administrateurs.add(membre)  # Ajouter le créateur comme admin
                image = image_form.save(commit=False)
                com.image =  image
                image.save()
                com.save()

                personnes_formset.save()
                lieux_formset.save()

                messages.success(request, "Communauté créée avec succès.")
                return redirect("show_communaute", com.id)

            else:            
                messages.error(request, "Erreur lors de la création. Vérifiez les champs.")

        except PermissionDenied as e:
            # messages.error(request, str(e))
            # form = AssociationForm(user=user)
            messages.error(request, f"Vous n'avez pas les droits nécessaires {str(e)} ")
            # return redirect('upgrade_abonnement')   

    else:
        # GET : formulaires vides
        form = CommunauteForm()
        histoires_formset = MiniHistoireFormSet(instance=Communaute(), prefix='mini_histoire')
        rois_formset      = RoiFormSet(instance=Communaute(), prefix='rois_communaute')
        personnes_formset = PersonneFormSet(instance=Communaute(), prefix='personnes')
        lieux_formset     = LieuFormSet(instance=Communaute(), prefix='lieux')
        image_form = ImageForm()

    context = {
        'form': form,
        'histoires_formset': histoires_formset,
        'rois_formset': rois_formset,
        'personnes_formset': personnes_formset,
        'lieux_formset': lieux_formset,
        'image_form': image_form,
        'titre': "Créer une nouvelle communauté",
        'action': "Créer",
    }

    return render(request, "archcore/new_communaute.html", context)

def add_communaute0(request):

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

def upload_image(request):
    if request.method == "POST" and request.FILES.get("image"):
        image = Image.objects.create(
            fichier=request.FILES["image"],
            nom=request.POST.get("nom", "")
        )
        return JsonResponse({
            "id": image.id,
            "url": image.fichier.url
        })
    return JsonResponse({"error": "Erreur upload"}, status=400)

def show_galerie(request, id):
    galerie = get_object_or_404(Galerie, pk=id)
    return render(request, "usercore/show_galerie.html", { "galerie":galerie  })

def show_galerie_asso(request, id):
    asso = get_object_or_404(Association, pk=id)
    galerie = Galerie.objects.filter(association=asso).first()
    if galerie is None:
        messages.warning(request, "Aucune galerie n'est associée à cette association.")
        return redirect("show_association", id=asso.id)
    
    return render(request, "usercore/show_galerie_asso.html", { "galerie":galerie, "association": asso })

def update_galerie(request, id):

    galerie = get_object_or_404(Galerie, id=id)
    if request.method == "POST":
        form = GalerieForm(request.POST, instance=galerie)
        images_ids = request.POST.getlist("images_ids[]")

        if form.is_valid():
            galerie = form.save()
            galerie.images.set(images_ids)
            return redirect("show_galerie", galerie.id)

    else:
        form = GalerieForm(instance=galerie)

    return render(
        request,
        "usercore/update_galerie.html",
        {
            "form": form,
            "galerie": galerie,
            "images": galerie.images.all()
        }
    )

def add_galerie(request):
    
    if request.method == "POST":
        form = GalerieForm(request.POST)
        images_ids = request.POST.getlist("images_ids[]")

        if form.is_valid():  
            galerie = form.save() 
            galerie.save()            
            galerie.images.set(images_ids)
            
            return redirect("show_galerie",galerie.id )
 
    else:
        form = GalerieForm()

    return render(request, "usercore/new_galerie.html", { "form":form  })

# Afficher l'histoire d'une communauté
@require_http_methods(["GET"])
def community_history(request, community_id):
    com = Communaute.objects.get(id=community_id)
    # histoires = com.histoires.all().order_by('-date', 'nom')
    histoires = MiniHistoire.objects.filter(communaute=com).order_by('-date', 'nom')
    
    # histoires = com.histoires.filter(
    #     models.Q(nom__isnull=False) & ~models.Q(nom="") |
    #     models.Q(description__isnull=False) & ~models.Q(description="")
    # ).order_by('-date', 'nom')

    context = {
        'community_id': community_id,
        'community_name': com.nom,
        "histoires":  histoires,
        'history': {
            'origin': com.origine,
            'chief': com.chef.nomcomplet if com.chef else "Inconnu",
            'description': com.histoire, 
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
        'map_zoom': 12, 
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
    }
    return render(request, 'archcore/king_list.html', context)
