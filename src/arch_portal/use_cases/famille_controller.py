
from django.shortcuts import redirect, render, get_object_or_404
from arch_portal.domain.forms.famille import FamilleForm
from arch_portal.domain.forms.image import ImageForm
from arch_portal.domain.models.communaute import Communaute
from arch_portal.domain.models.famille import Famille
from arch_portal.domain.models.pagefamille import Pagefamille
from arch_portal.domain.models.role import Role
from arch_portal.domain.models.membre import Membre
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponseForbidden, JsonResponse 
from collections import defaultdict
from django.contrib import messages


def page_famille(request, id):
    famille = get_object_or_404(Famille, pk=id)
    return render(request, 'famille/page_famille.html', {'famille': famille})

def add_page(request, id):

    famille = get_object_or_404(Famille, pk=id)    
    # Vérification des droits
    # if not (famille.administrateurs.filter(id=request.user.id).exists()):
    #     messages.error(request, "Vous n'avez pas le droit d'ajouter une histoire à cette famille.")
    #     return redirect('show_famille', id=famille.id)
    
    if request.method == "POST":
        titre = request.POST.get("titre", "").strip()
        contenu = request.POST.get("contenu", "").strip()
        ordre = request.POST.get("ordre", "10")
        
        if not titre or not contenu:
            messages.error(request, "Le titre et le contenu sont obligatoires.")
        else:
            try:
                ordre = int(ordre)
            except:
                ordre = 10
                
            Pagefamille.objects.create(
                famille=famille,
                titre=titre,
                contenu=contenu,
                ordre=ordre,
                # created_by=request.user  ← si tu ajoutes ce champ plus tard
            )
            messages.success(request, "Histoire détaillée ajoutée avec succès !")
            return redirect('show_famille', id=famille.id)
    
    # GET → on ne devrait normalement pas arriver ici car c'est une modal
    return redirect('show_famille', id=id)

def edit_famille(request, id):
    
    famille = get_object_or_404(Famille, id=id)
    image_instance = famille.image if hasattr(famille, 'image') else None

    if request.method == 'POST':
        form = FamilleForm(request.POST, instance=famille)
        image_form = ImageForm(request.POST, request.FILES, instance=image_instance)

        if form.is_valid() and image_form.is_valid():
            famille = form.save()

            if( image_form.has_changed() or image_form.cleaned_data.get("fichier")):
                image = image_form.save(commit=False)
                famille.image =  image
                image.save()            
 
            messages.success(request, "Famille et images modifiées avec succès.")
            return redirect('show_famille', id=id)
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")

    else:
        # GET : formulaire vierge + formset pré-rempli avec les images existantes
        form = FamilleForm(instance=famille)
        image_form = ImageForm(instance=image_instance)

    return render(request, 'famille/edit_famille.html', {'famille': famille, 'form': form , 'image_form': image_form,})

def famille_generations(request, famille_id):

    famille = get_object_or_404(Famille, id=famille_id)
    membres = Membre.objects.filter( familles=famille ).select_related('nompere', 'nommere')

    generations = defaultdict(list)
    for membre in membres:
        gen = membre.generation
        # On met None dans une clé spéciale (ex: 0 ou -1 ou une string)
        key = gen if gen is not None else 0   # ← ou -1, ou "Inconnu"
        generations[key].append(membre)
        generations[membre.generation].append(membre)

    generations = dict(sorted(
        generations.items(),  
        key=lambda item: item[0] if isinstance(item[0], int) else -999
        )
    )

    context = {
        "famille": famille,
        "generations": generations,
        "has_unknown_generation": 0 in generations
    }
    return render(request, "famille/famille_generations.html", context)

def build_family_tree(membre):
    return {
        "id": membre.id,
        "nom": membre.nomcomplet,
        "pere": build_family_tree(membre.nompere) if membre.nompere else None,
        "mere": build_family_tree(membre.nommere) if membre.nommere else None,
    }

def build_tree(membre):

    children = []

    if membre.nompere:
        children.append(build_tree(membre.nompere))

    if membre.nommere:
        children.append(build_tree(membre.nommere))

    return {
        "name": membre.nomcomplet,
        "id": membre.id,
        "children": children
    }

    # return {
    #     "name": membre.nomcomplet,
    #     "id": membre.id,
    #     "children": [
    #         build_tree(membre.nompere) if membre.nompere else None,
    #         build_tree(membre.nommere) if membre.nommere else None
    #     ]
    # }

def famille_arbre(request, famille_id):

    famille = get_object_or_404(Famille, id=famille_id)
    racines = Membre.objects.filter( familles=famille,  nompere__isnull=True,  nommere__isnull=True  )
    arbres = [build_family_tree(m) for m in racines]

    context = {
        "famille": famille,
        "arbres": arbres
    }
    return render(request, "famille/famille_arbre.html", context)

def famille_arbre_graphique(request, famille_id):

    famille = get_object_or_404(Famille, id=famille_id)
    racines = Membre.objects.filter( familles=famille,  nompere__isnull=True,  nommere__isnull=True  )
    arbres = [build_tree(m) for m in racines]

    context = {
        "famille": famille,
        "tree_data": json.dumps(arbres)
    }
    return render(request, "famille/arbre_graphique.html", context)

def listfamilles(request, id, mode=0):
   
    familles = Famille.objects.filter(communaute=id)
    lib = Communaute.objects.get(id=id) 

    # userid = request.session.get("userid","")
    # if not userid :
    #     # print(f" user id { userid } ")
    #     return redirect("login" )

    # user = Membre.objects.get(id=userid)
    # appartient=False
    # if ( user in com.membres_communaute.all()):
    #     appartient = True

    if not mode: 
        return render(request, "archcore/listfamilles_tab.html", { "familles" : familles, "communaute" : lib } )
    return render(request, "archcore/listfamilles.html", { "familles" : familles, "communaute" : lib } )

def show_famille(request,id):
    fam = Famille.objects.get(id=id)

    if not request.session.get("userid","") :
        return redirect("login" )
    
    #  ce utilisateur ne peut voir les info detaillée de la famille que si il appartient à la famille ou a des droits
    userid = request.session.get("userid","")
    user = Membre.objects.get(id=userid)
    appartient=False
    if ( user in fam.membres_famille.all()):
        appartient = True
    
    return render(request, "archcore/showfamille.html", {"famille" : fam, "appartient" : appartient} )


def show_admin_fam(request,id):
    
    com = Famille.objects.get(id=id) 
    return render(request, "archcore/listadminfam.html", {"admins": com.administrateurs.all(), "famille": com})


@csrf_exempt
def add_admin_fam(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax :
        if request.method == "POST" :
            data = json.loads(request.body.decode('utf-8'))
            if not request.session.get("userid","") :
                return redirect("login" )
    
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
