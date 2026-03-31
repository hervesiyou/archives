import json

# from django.core.serializers import serialize
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from arch_portal.domain.models.wallet import Wallet
from arch_portal.domain.exceptions.membre_exception import MembreException
from arch_portal.use_cases.services.core import compute_sha1
from arch_portal.domain.forms.membre import MembreForm,UsersLoginForm,UsersSubscribeForm
from arch_portal.domain.models.membre import Membre
from arch_portal.domain.models.histoire import MiniHistoire

from arch_portal.domain.models.image import Image
from django.http import  JsonResponse
  
from arch_portal.domain.forms.membre import MembreEditForm

# from arch_portal.domain.serializers import MembreSerializer

def subscribe(request):
    if request.method == "POST":
        form = UsersSubscribeForm(request.POST)
        if form.is_valid():  
            user = form.save()
        return redirect("login")
    else:
        form = UsersSubscribeForm()
    return render(request, "usercore/subscribe.html", {"form":form})   

def log_out(request):
    del request.session["username"]
    del request.session["userid"]
    del request.session["nomcomplet"]
    request.session.flush()
    return redirect("login")

def log_user(request):
    if request.method == "POST":
        form = UsersLoginForm(request.POST)
        if form.is_valid():
            # print(compute_sha1( form.cleaned_data["pwd"]) )
            user = Membre.objects.filter(
                login=form.cleaned_data["login"],
                pwd=compute_sha1(form.cleaned_data["pwd"]),
            ).first()

            if user != None:

                request.session["username"] = user.login 
                request.session["userrights"] =  user.get_rights()
                request.session["nomcomplet"] = user.nomcomplet
                # request.session["user"] = user
                request.session["userid"] = user.id
                request.session.modified = True
                messages.info(request,f"Bienvenue { user.nomcomplet }")
                return redirect("home" )
            else:
                messages.info(request,f" Desolé { form.cleaned_data['login']}  nous est inconnu !")
    else:
        request.session.get("username1","")
        request.session.get("userid1",0) 
        form = UsersLoginForm()

    return render(request, "usercore/login.html", {"form":form})

def show_user_messages(request):
    if(request.session["userid"]!=None):
        user=Membre.objects.get(id=request.session["userid"])
        
        if(user != None):
            return render(request, "usercore/listmessages.html", {"user":user, })
        else:
            raise MembreException( f" Membre {request.session['userid']} introuvable ")  
    else:
        return redirect("login")

def user_abonnement(request):
    userid = request.session.get("userid", None)
    if(userid is not  None):
        user = Membre.objects.get(id=request.session["userid"])
        
        if(user != None):
            return render(request, "usercore/abonnement.html", {"user":user, })
        else:
            raise MembreException( f" Membre {request.session['userid']} introuvable ")  
    else:
        return redirect("login")

def show_user_home(request):
    userid = request.session.get("userid", None)
    if(userid is not  None):
        user = Membre.objects.get(id=request.session["userid"])
        if(user != None):
            wallet = Wallet.objects.filter(membre_id=user.id ).first()
            # print( user.id , wallet)
            return render(request, "usercore/home.html", {"user":user, "wallet":wallet})
        else:
            raise MembreException( f" Membre {request.session['userid']} introuvable ")  
    else:
        return redirect("login")

def show_user_famadmin(request):
    if(request.session["userid"]!=None):
        user=Membre.objects.get(id=request.session["userid"])
        if(user != None):
            adfamilles = user.familles.all()
            fams = user.fam_admins.all()
            return render(request, "usercore/listmyfamadmin.html", {"user":user, "familles":fams, "adfamilles": adfamilles})
        else:
            raise MembreException( f" Membre {request.session['userid']} introuvable ")  
    else:
        return redirect("login")

def show_user_comadmin(request):
    if(request.session["userid"]!=None):
        user=Membre.objects.get(id=request.session["userid"])
        if(user != None):
            coms = user.com_admins.all()
            adcoms = user.communautes.all()
            return render(request, "usercore/listmycomadmin.html", {"user":user , "communautes": coms, "adcommunautes":adcoms})
        else:
            raise MembreException( f" Membre {request.session['userid']} introuvable ")  
    else:
        return redirect("login")

def show_user_assoadmin(request):
    if(request.session["userid"] != None):
        user = Membre.objects.get(id=request.session["userid"])
        if(user != None):
            adasso = user.asso_admins.all()
            assos = user.associations.all()
            return render(request, "usercore/listmyassoadmin.html", {"user":user , "associations": assos, "adassos":adasso })
        else:
            raise MembreException( f" Membre {request.session['userid']} introuvable ")  
    else:
        return redirect("login")


def show_user(request,id):
    # membre = Membre.objects.get(id=id)
    membre = Membre.objects.prefetch_related('mini_histoire').get(id=id)
    return render(request, "usercore/show_user.html", {"membre":membre})

def add_user(request):

    if request.method == "POST":
        form = MembreForm(request.POST)
        # print(form.errors)
        if form.is_valid():  
            com = form.save() 
            com.save()
            return redirect("show_user",com.id )
    else:
        form = MembreForm()

    return render(request, "usercore/newuser.html", {"form":form})

def upload_image_histoire(request):
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



def edit_user(request, id):
    membre = get_object_or_404(Membre, id=id)

    if request.method == 'POST':
        form = MembreEditForm(request.POST, request.FILES, instance=membre)
        

        if form.is_valid():
            form.save()            
            messages.success(request, "✅ Membre mis à jour avec succès")
            return redirect('show_user', id=membre.id)
        else:
            messages.error(request, f"❌ Veuillez corriger les erreurs {form.errors} du formulaire.")
    else:
        form = MembreEditForm(instance=membre)

    return render(request, 'usercore/edit_user.html', {
        'form': form,
        'membre': membre
    })

def add_histoire_membre(request, id):

    user = get_object_or_404(Membre, pk=id)   
    
    if request.method == "POST":
        lieu = request.POST.get("lieu", "").strip()
        titre = request.POST.get("nom", "").strip()
        contenu = request.POST.get("description", "").strip()
        ordre = request.POST.get("ordre", "10")

        #  je recupere les id des image de la minihistoire uploadé
        images_ids = request.POST.getlist("images_ids[]")
        
        if not titre or not contenu:
            messages.error(request, "Le titre et le contenu sont obligatoires.")
        else:
            try:
                ordre = int(ordre)
            except:
                ordre = 10
                
            histoire = MiniHistoire.objects.create(
                membre=user,
                lieu=lieu,
                nom=titre,
                description=contenu,
                ordre=ordre, 
            )

            histoire.images.set(images_ids)
            messages.success(request, "Histoire détaillée ajoutée avec succès !")
            return redirect('show_user', id=user.id)
    
    # GET → on ne devrait normalement pas arriver ici car c'est une modal
    return redirect('show_user', id=id)