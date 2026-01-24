from django.shortcuts import render, redirect 
from django.conf import settings
from arch_portal.domain.exceptions.membre_exception import MembreException
from arch_portal.domain.models.salleattentefamille import SalleAttenteFamille
from arch_portal.domain.models.communaute import Communaute
from arch_portal.domain.models.famille import Famille
from arch_portal.domain.models.membre import Membre
from arch_portal.domain.models.message import Message
from arch_portal.domain.models.association import Association
from arch_portal.domain.models.salleattentecommunaute import SalleAttenteCommunaute
from arch_portal.domain.models.salleattenteassociation import SalleAttenteAssociation
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponseForbidden, JsonResponse
from datetime import date

def index(request): 
    return render(request, "base.html" )

def contact(request): 
    if request.method == "POST":
        # traitement du formulaire
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        # ici tu peux sauvegarder le message ou l'envoyer par email
        return redirect("contact")  # page de succès

    return render(request, "includes/contact.html", {
        # "HCAPTCHA": getattr(settings, "APP_HCAPTCHA", None),
        # "ORANGE": getattr(settings, "NO_ORANGE", None),
        # "MTN": getattr(settings, "NO_MTN", None),
        # "SARA": getattr(settings, "NO_SARA", None),
        # "VERSION": "1.0.1"
    })
    # return render(request, "includes/contact.html" )

def show_com_salle(request,id):
    if(request.session["userid"]!=None):
        user = Membre.objects.get(id=request.session["userid"])
        if(user != None):
            com = Communaute.objects.get(id=id)

            users = SalleAttenteCommunaute.objects.filter(communaute=com)
            return render(request, "usercore/salleattentecom.html", { "communaute": com, "users":users})
        else:
            raise MembreException( f" Membre {request.session['userid']} introuvable ")  
    else:
        return redirect("login")

def show_fam_salle(request,id):
    if(request.session["userid"]!=None):
        user = Membre.objects.get(id=request.session["userid"])
        if(user != None):
            com = Famille.objects.get(id=id)

            users = SalleAttenteFamille.objects.filter(famille=com)
            return render(request, "usercore/salleattentefam.html", { "famille": com, "users":users})
        else:
            raise MembreException( f" Membre {request.session['userid']} introuvable ")  
    else:
        return redirect("login")

def show_asso_salle(request,id):
    if(request.session["userid"]!=None):
        user = Membre.objects.get(id=request.session["userid"])
        if(user != None):
            com = Association.objects.get(id=id)

            users = SalleAttenteAssociation.objects.filter(association=com)
            return render(request, "usercore/salleattenteasso.html", { "association": com, "users":users})
        else:
            raise MembreException( f" Membre {request.session['userid']} introuvable ")  
    else:
        return redirect("login")


@csrf_exempt
def valide_salleatt(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax :
        if request.method == "POST" :
            data = json.loads(request.body.decode('utf-8'))
            userid = request.session.get("userid","") 
            
            if data.get('salle') is None:
                return JsonResponse({'status': False ,"message": "Famille incorrecte"})
            else: 
                if userid is None:
                    return JsonResponse({'status': False ,"message": "Merci de vous connecter avant tout abonnement !"})
                else:
                    if data.get('direction') is None:
                        return JsonResponse({'status': False ,"message": "Probleme de procedure !"})
                    else:
                        user = Membre.objects.get(id=userid)
                        if( data.get("direction") == "FAM"):
                            salle = SalleAttenteFamille.objects.get(id=data.get("salle"))
                            salle.famille.membres_famille.add(salle.personne)
                            mes = Message(
                                sujet=f" Votre validation d'accès à {salle.famille.nom} ",
                                contenu=f" Un administrateur à validé votre accès à la FAMILLE : {salle.famille.nom}, vous pouvez desormais y acceder .",
                                date_ajout=date.today()
                            )
                            mes.save()
                            salle.personne.messages.add( mes )
                            salle.personne.save()
                            salle.famille.save()
                            message = f"Merci {salle.personne.nomcomplet} , a été autorisé a adherer à  {salle.famille.nom} "
                        else:
                            if( data.get("direction") == "COM"):
                                salle = SalleAttenteCommunaute.objects.get(id=data.get("salle"))
                                salle.communaute.membres_communaute.add(salle.personne)
                                mes = Message(
                                    sujet=f" Votre validation d'accès à {salle.communaute.nom} ",
                                    contenu=f" Un administrateur à validé votre accès à la COMMUNAUTE : {salle.communaute.nom}, vous pouvez desormais y acceder .",
                                    date_ajout=date.today()
                                )
                                 
                                mes.save()
                                salle.personne.messages.add( mes )
                                salle.personne.save()
                                salle.communaute.save()
                                message = f"Merci {salle.personne.nomcomplet} , a été autorisé a adherer à  {salle.communaute.nom} "
                            else:
                                if( data.get("direction") == "ASSO"):
                                    salle = SalleAttenteAssociation.objects.get(id=data.get("salle"))
                                    salle.association.membres_association.add(salle.personne)
                                    mes = Message(
                                        sujet=f" Votre validation d'accès à {salle.association.nom} ",
                                        contenu = f" Un administrateur à validé votre accès à l'ASSOCIATION : {salle.association.nom}, vous pouvez desormais y acceder .",
                                        date_ajout = date.today()
                                    )
                                    
                                    mes.save()
                                    salle.personne.messages.add( mes )
                                    salle.personne.save()
                                    salle.association.save()
                                    message = f"Merci {salle.personne.nomcomplet} , a été autorisé a adherer à  {salle.association.nom} "
                                else:
                                    return JsonResponse({'status': False ,"message": "Probleme de procedure de validation !"})
                        
                        salle.validateur =  user
                        salle.date_validation =  date.today()
                        salle.valide = True
                        
                        salle.save()
                        #  ici je peux aussi envoyer un mail à l'utilisateur
                        return JsonResponse({'status': True ,"message": message})
               

@csrf_exempt
def add_user_salleattfam(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax :
        if request.method == "POST" :
            data = json.loads(request.body.decode('utf-8'))
            userid = request.session.get("userid","")
            # user = f' un: {request.session.get("username","")} ,id: {request.session.get("userid","")},n: {request.session.get("nomocomplet","")}'
            # print(data ,data.get("code"))
            
            if data.get('famid') is None:
                return JsonResponse({'status': False ,"message": "Famille incorrecte"})
            else: 
                if userid is None:
                    return JsonResponse({'status': False ,"message": "Merci de vous connecter avant tout abonnement !"})
                else:
                    user = Membre.objects.get(id=userid)
                    famille = Famille.objects.get(id=data.get("famid"))
                
                    ab = SalleAttenteFamille.objects.filter(personne=user, famille=famille)
                    # print(ab, plan, user)
                    if len(ab) == 0: 
                        ab = SalleAttenteFamille( 
                            personne = user,
                            famille= famille, 
                        )
                        ab.save() 
                        message = f"Merci {user.nomcomplet} , votre sollitation d'adherer à la famille {famille.nom} a été prise en compte, un administrateur vous reviendrait dès la fin de l'etude"
                        
                        return JsonResponse({'status': True ,"message": message})
                    else:
                        return JsonResponse({'status': False ,"message": "Desolé, vous avez etes deja dans la salle d'attente !"})

@csrf_exempt
def add_user_salleattcom(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax :
        if request.method == "POST" :
            data = json.loads(request.body.decode('utf-8'))
            userid = request.session.get("userid","") 
            
            if data.get('comid') is None:
                return JsonResponse({'status': False ,"message": "Communauté incorrecte"})
            else: 
                if userid is None:
                    return JsonResponse({'status': False ,"message": "Merci de vous connecter avant tout abonnement !"})
                else:
                    user = Membre.objects.get(id=userid)
                    com = Communaute.objects.get(id=data.get("comid"))
                
                    ab = SalleAttenteCommunaute.objects.filter(personne=user, communaute=com)
                    # print(ab, plan, user)
                    if len(ab) == 0: 
                        ab = SalleAttenteCommunaute( 
                            personne = user,
                            communaute = com, 
                        )
                        ab.save() 
                        message = f"Merci {user.nomcomplet} , votre sollitation d'adherer à la communauté {com.nom} a été prise en compte, un administrateur vous reviendrait dès la fin de l'etude"
                        
                        return JsonResponse({'status': True ,"message": message})
                    else:
                        return JsonResponse({'status': False ,"message": "Desolé, vous avez etes deja dans la salle d'attente !"})

def faq(request):
    return render(request, "archcore/faq.html", {} )

def faqindex(request):
    return render(request, "includes/faqindex.html", {} )


@csrf_exempt
def add_user_salleattasso(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax :
        if request.method == "POST" :
            data = json.loads(request.body.decode('utf-8'))
            userid = request.session.get("userid","") 
            
            if data.get('assoid') is None:
                return JsonResponse({'status': False ,"message": "Association incorrecte"})
            else: 
                if userid is None:
                    return JsonResponse({'status': False ,"message": "Merci de vous connecter avant tout abonnement !"})
                else:
                    user = Membre.objects.get(id=userid)
                    asso = Association.objects.get(id=data.get("assoid"))
                
                    ab = SalleAttenteAssociation.objects.filter(personne=user, association=asso)
                    # print(ab, plan, user)
                    if len(ab) == 0: 
                        ab = SalleAttenteAssociation( 
                            personne = user,
                            association = asso, 
                        )
                        ab.save() 
                        message = f"Merci {user.nomcomplet} , votre sollitation d'adherer à l'association {asso.nom} a été prise en compte, un administrateur vous reviendrait dès la fin de l'etude"
                        
                        return JsonResponse({'status': True ,"message": message})
                    else:
                        return JsonResponse({'status': False ,"message": "Desolé, vous avez etes deja dans la salle d'attente !"})



