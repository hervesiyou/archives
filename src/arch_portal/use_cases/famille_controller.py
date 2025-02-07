
from django.shortcuts import redirect, render
from arch_portal.domain.forms.famille import FamilleForm
from arch_portal.domain.models.communaute import Communaute
from arch_portal.domain.models.famille import Famille
from arch_portal.domain.models.role import Role
from arch_portal.domain.models.membre import Membre
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponseForbidden, JsonResponse

def listfamilles(request, id):
   
    livres = Famille.objects.filter(communaute=id)
    lib = Communaute.objects.get(id=id) 
    return render(request, "archcore/listfamilles.html", { "familles" : livres, "communaute" : lib } )

def show_famille(request,id):
    fam = Famille.objects.get(id=id)
    #  ce utilisateur ne peut voir les info detaillée de la famille que si il appartient à la famille ou a des droits
    userid = request.session.get("userid","")
    user = Membre.objects.get(id=userid)
    appartient=False
    if ( user in fam.membres_famille.all()):
        appartient = True
    # print( "membres: {}".format(liv.get_members()) )
    return render(request, "archcore/showfamille.html", {"famille" : fam, "appartient" : appartient} )


def show_admin_fam(request,id):
    com = Famille.objects.get(id=id)
    # print(com.administrateurs.all())
    return render(request, "archcore/listadminfam.html", {"admins": com.administrateurs.all(), "famille": com})


@csrf_exempt
def add_admin_fam(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax :
        if request.method == "POST" :
            data = json.loads(request.body.decode('utf-8'))
            userid = request.session.get("userid","")
            # user = f' un: {request.session.get("username","")} ,id: {request.session.get("userid","")},n: {request.session.get("nomocomplet","")}'
             
            if data.get('famid') is None:
                return JsonResponse({'status': False ,"message": "Famille incorrecte !"})
            else:
                if data.get("adminid") is None:
                    return JsonResponse({'status': False ,"message": "Identification utilisateur incorrecte"})
                else:
                    if userid is None:
                        return JsonResponse({'status': False ,"message": "Merci de vous connecter avant tout abonnement !"})
                    else:
                        user = Membre.objects.get(id=data.get("adminid"))
                        com = Famille.objects.get(id=data.get("famid"))
                        role = Role.objects.get(nom="ADMIN")
                        # print(role, user)
                        user.role.add(role)
                        user.save()
                        com.administrateurs.add(user)
                        com.save()

                        return JsonResponse({'status': True ,"message": f"{user.nomcomplet} a été ajouté comme administrateur à la Famille {com.nom}"})


def add_famille(request):
    
    if request.method == "POST":
        form = FamilleForm(request.POST)
        if form.is_valid():  
            com = form.save() 
            com.save()
            return redirect("show_famille",com.id )
    else:
        form = FamilleForm()

    return render(request, "archcore/new_famille.html", { "form":form  })
