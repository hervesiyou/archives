
from django.shortcuts import redirect, render
from django.contrib import messages
from arch_portal.domain.exceptions.membre_exception import MembreException
from arch_portal.use_cases.services.core import compute_sha1
from arch_portal.domain.forms.membre import MembreForm,UsersLoginForm,UsersSubscribeForm
from arch_portal.domain.models.membre import Membre


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
            user = Membre.objects.filter(
                login=form.cleaned_data["login"],
                pwd=compute_sha1(form.cleaned_data["pwd"]),
            ).first()
             
            if user != None:
                request.session["username"] = user.login 
                request.session["nomcomplet"] = user.nomcomplet 
                request.session["userid"] = user.id
                request.session.modified = True
                messages.info(request,f"Bienvenue { user.nomcomplet }")
                return redirect("home" )
            else:
                messages.info(request,f"Desolé { form.cleaned_data["login"]} nous est inconnu !")
    else:
        request.session.get("username1","")
        request.session.get("userid1",0) 
        form = UsersLoginForm()
 
    return render(request, "usercore/login.html", {"form":form})

def show_user_home(request):
    if(request.session["userid"]!=None):
        user=Membre.objects.get(id=request.session["userid"])
        if(user != None):
            return render(request, "usercore/home.html", {"user":user})
        else:
            raise MembreException( f" Membre {request.session["userid"]} introuvable ")  
    else:
        return redirect("login")

def show_user(request,id):
    pass
def add_user(request):
    
    if request.method == "POST":
        form = MembreForm(request.POST)
        if form.is_valid():  
            com = form.save() 
            com.save()
        return redirect("show_user",com.id )
    else:
        form = MembreForm()

    return render(request, "usercore/newuser.html", {"form":form})

