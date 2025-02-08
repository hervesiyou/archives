from django.shortcuts import render, redirect 
from arch_portal.domain.models.salleattentefamille import SalleAttenteFamille
from arch_portal.domain.models.communaute import Communaute
from arch_portal.domain.models.famille import Famille
from arch_portal.domain.models.membre import Membre
from arch_portal.domain.models.salleattentecommunaute import SalleAttenteCommunaute
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponseForbidden, JsonResponse


def index(request): 
    return render(request, "base.html" )

def show_com_salle(request,id):
    if(request.session["userid"]!=None):
        user = Membre.objects.get(id=request.session["userid"])
        if(user != None):
            com = Communaute.objects.get(id=id)

            users = SalleAttenteCommunaute.objects.filter(communaute=com)
            return render(request, "usercore/salleattentecom.html", { "communaute": com, "users":users})
        else:
            raise MembreException( f" Membre {request.session["userid"]} introuvable ")  
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
            raise MembreException( f" Membre {request.session["userid"]} introuvable ")  
    else:
        return redirect("login")

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




