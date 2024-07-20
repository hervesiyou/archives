from django.shortcuts import render, redirect
from coreapp.forms.membre import MembreForm
from coreapp.forms.galerie import GalerieForm
from coreapp.models.communaute import Communaute
from coreapp.models import *


# Create your views here.
def index(request): 
    return render(request, "base.html" )

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

def show_com(request,id):
    com = Communaute.objects.get(id=id)
    return render(request, "show_com.html", {"communaute":com})

def log_out(request):

    del request.session["username"]
    del request.session["userid"]
    request.session.flush()

    return redirect("index")
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

def log_user(request):
    pass
    # if request.method == "POST":
    #     form = UsersLoginForm(request.POST)

    #     if form.is_valid():
    #         user = Users.objects.get(login=form.cleaned_data["login"],pwd = compute_sha1(form.cleaned_data["pwd"]) )
    #         if user:
    #             request.session["username"] = user.login
    #             # request.session.get("username1",user.login)
    #             # request.session.get("userid1",user.id) 
    #             request.session["userid"] = user.id
    #             request.session.modified = True
    #             return redirect("home" )

    # else:
    #     request.session.get("username1","")
    #     request.session.get("userid1",0) 
    #     form = UsersLoginForm()
 
    # return render(request, "login.html", {"form":form})
