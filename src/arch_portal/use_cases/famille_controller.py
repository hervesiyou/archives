
from django.shortcuts import redirect, render, get_object_or_404
from arch_portal.domain.forms.famille import FamilleForm
from arch_portal.domain.forms.image import ImageForm
from arch_portal.domain.models.communaute import Communaute
from arch_portal.domain.models.galerie import Galerie
from arch_portal.domain.models.famille import Famille
# from arch_portal.domain.models.salleattentefamille import SalleAttenteFamille
from arch_portal.domain.models.pagefamille import Pagefamille
from arch_portal.domain.models.role import Role
from arch_portal.domain.models.membre import Membre
from django.views.decorators.csrf import csrf_exempt
import json
from django.urls import reverse
from django.http import HttpResponseForbidden, JsonResponse 
from collections import defaultdict
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from arch_portal.use_cases.services.subscription_service import check_abonnement_permission, get_membre_from_session
from collections import defaultdict, deque

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
    
    if not request.session.get("userid","") :
        return redirect("login" )
    
    user = request.session['userid']
    user = get_object_or_404(Membre, pk=user)
    
    famille = get_object_or_404(Famille, id=id)
    admins = famille.administrateurs.all()
    # si le user connecté n'est pas administrateur
    if not ( user in famille.administrateurs.all() or ("ADD_FAMILLE" in request.session["userrights"]) ):
        messages.error(request, "Vous n'avez pas le droit de modifier cette famille.")
        return redirect('show_famille', id=famille.id)
    
    image_instance = famille.image if hasattr(famille, 'image') else None

    if request.method == 'POST':
        form = FamilleForm(request.POST, instance=famille)
        image_form = ImageForm(request.POST, request.FILES, instance=image_instance)

        if form.is_valid() and image_form.is_valid():
            famille = form.save()

            if( image_form.cleaned_data.get("fichier") != None and len(image_form.cleaned_data.get('fichier')) > 0 ):
                # if image_form.has_changed() :
                image = image_form.save(commit=False)
                famille.image =  image
                image.save()
                famille.save()            
 
            messages.success(request, "Famille et images modifiées avec succès.")
            return redirect('show_famille', id=id)
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")

    else:
        # GET : formulaire vierge + formset pré-rempli avec les images existantes
        form = FamilleForm(instance=famille)
        image_form = ImageForm(instance=image_instance)

    return render(request, 'famille/edit_famille.html', {'famille': famille, 'administrateurs':len(admins), 'admins':admins, 'form': form , 'image_form': image_form,})

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

def build_family_tree_levels(famille):

    membres = Membre.objects.filter( familles=famille ).select_related("nompere", "nommere")

    nodes = {}
    children_map = defaultdict(list)

    # 1. nodes
    for m in membres:
        nodes[m.id] = {
            "id": m.id,
            "nom": m.nomcomplet,
            "photo": m.photo.url if m.photo else None,
            "enfants": []
        }

    # 2. relations parent -> enfants
    for m in membres:
        if m.nompere_id and m.nompere_id in nodes:
            children_map[m.nompere_id].append(m.id)

        if m.nommere_id and m.nommere_id in nodes:
            children_map[m.nommere_id].append(m.id)

    # 3. injecter enfants
    for parent_id, enfants_ids in children_map.items():
        nodes[parent_id]["enfants"] = enfants_ids

    # 4. trouver racines (pas de parent dans famille)
    all_children = set()
    for v in children_map.values():
        all_children.update(v)

    roots = [m.id for m in membres if m.id not in all_children]

    # fallback
    if not roots:
        roots = list(nodes.keys())

    # 5. BFS par niveaux
    levels = []
    visited = set()
    queue = deque([(r, 0) for r in roots])

    while queue:
        node_id, level = queue.popleft()

        if node_id in visited:
            continue
        visited.add(node_id)

        if len(levels) <= level:
            levels.append([])

        levels[level].append(nodes[node_id])

        for child_id in nodes[node_id]["enfants"]:
            queue.append((child_id, level + 1))

    return levels

def build_family(famille):
    # 1. Charger tous les membres de la famille en une seule requête
    membres = Membre.objects.filter( familles=famille ).select_related("nompere", "nommere")
    # 2. Indexation rapide
    nodes = {}
    enfants_map = defaultdict(list)

    for m in membres:
        nodes[m.id] = {
            "membre": m,
            "enfants": []
        }

    # 3. Construire relations parent -> enfants
    for m in membres:
        if m.nompere_id and m.nompere_id in nodes:
            enfants_map[m.nompere_id].append(nodes[m.id])

        if m.nommere_id and m.nommere_id in nodes:
            enfants_map[m.nommere_id].append(nodes[m.id])

    # 4. Injecter enfants dans nodes
    for parent_id, enfants in enfants_map.items():
        nodes[parent_id]["enfants"] = enfants

    # 5. Trouver les racines (sans parents dans la famille)
    racines = []
    for m in membres:
        if (m.nompere_id not in nodes) and (m.nommere_id not in nodes):
            racines.append(nodes[m.id])

    # fallback si racines mal définies
    if not racines:
        racines = list(nodes.values())

    return racines

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
        # racines = Membre.objects.filter( familles=famille,  nompere__isnull=True,  nommere__isnull=True  )
        # arbres = [build_family_tree(m) for m in racines]
        arbres = build_family(famille)
        niveaux = build_family_tree_levels(famille)

        context = {
            "famille": famille,
            "arbres": arbres, 
            "niveaux": niveaux,
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
    
    membre = get_membre_from_session(request) 
    if not membre:
        return redirect(f"{reverse('login')}?next={request.get_full_path()}")
    # si par defaut il n'a pas encore crée sa famille gratuite
    abo = membre.get_abonnement_actif()
    fam = membre.familles_creees.count()
    peut_creer_famille= False
    if abo and abo.plan is not None:
        peut_creer_famille= ( int(fam) < int(abo.plan.nbfamilles))

    if not mode: 
        return render(request, "archcore/listfamilles_tab.html", { "familles" : familles, "communaute" : lib , "peut_creer_famille":peut_creer_famille } )
    return render(request, "archcore/listfamilles.html", { "familles" : familles, "communaute" : lib , "peut_creer_famille":peut_creer_famille } )

def show_famille(request,id):
    fam = Famille.objects.get(id=id)

    if not request.session.get("userid","") :
        return redirect("login" )
    
    #  ce utilisateur ne peut voir les info detaillée de la famille que si il appartient à la famille ou a des droits
    userid = request.session.get("userid","")
    user = Membre.objects.get(id=userid)

    galerie = Galerie.objects.filter(famille=fam).first()
    appartient=False
    if ( user in fam.membres_famille.all()):
        appartient = True

    #  je check si c'est le createur ou un admin 
    gestionnaire=False
    if fam.createur == user or (user in fam.administrateurs.all()):
        gestionnaire = True
    
    return render(request, "archcore/showfamille.html", {"famille" : fam, "appartient" : appartient, "galerie" : galerie, "gestionnaire":gestionnaire } )


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
    # celui qui cree une famille est son administrateur par defaut        
    if request.method == "POST":
        try:
            check_abonnement_permission(request, 'famille')

            form = FamilleForm(request.POST)
            if form.is_valid():  
                if not request.session.get("userid","") :
                    return redirect("login" )

                com = form.save() 
                userid = request.session.get("userid","")
                user = Membre.objects.get(id=userid)
                com.administrateurs.add(user)
                #  je le met comme createur de la famille
                com.createur = user
                # je met cet utilisateur comme membre de cette famille
                user.familles.add(com)
                user.save()
                com.save()

                return redirect("show_famille",com.id )
        except PermissionDenied as e:
                messages.error(request, str(e))
                return redirect("add_famille")
    else:
        form = FamilleForm()

        return render(request, "archcore/new_famille.html", { "form":form  })
