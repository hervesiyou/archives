from django.shortcuts import redirect, render
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
                            message = '''
                            Merci de faire le depot au numero 690000000 pour OM et  677777777 pour MOMO pour l'activation de votre compte !
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
                       

def abonement_archive(request): 
    plans = Plan.objects.filter(appli="COM")
    return render(request, "archcore/abonement.html", {"plans" : plans} )

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


def listassociations(request, id):
    assos = Association.objects.filter(communaute=id)
    com = Communaute.objects.get(id=id)
    return render(request, "archcore/listassociations.html", {"associations": assos, "communaute": com})

def add_association(request):
    if request.method == "POST":
        form = AssociationForm(request.POST)
        if form.is_valid():  
            com = form.save() 
            com.save()
            
            return redirect("show_association",com.id )
    else:
        form = AssociationForm()

    return render(request, "archcore/new_association.html", { "form":form  })
 

def show_communaute(request,id):
    com = Communaute.objects.get(id=id)
    #  ce utilisateur ne peut voir les info detaillée de la famille que si il appartient à la famille ou a des droits
    userid = request.session.get("userid","")
    user = Membre.objects.get(id=userid)
    appartient=False
    if ( user in com.membres_communaute.all()):
        appartient = True

    return render(request, "archcore/show_com.html", {"communaute":com, "appartient" : appartient})

def show_admin_com(request,id):
    com = Communaute.objects.get(id=id)
    print(com.administrateurs.all())
    return render(request, "archcore/listadmincom.html", {"admins": com.administrateurs.all(), "communaute": com})



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
