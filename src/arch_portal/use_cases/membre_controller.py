
from django.shortcuts import redirect, render
from arch_portal.use_cases.services.core import compute_sha1
from arch_portal.domain.forms.membre import MembreForm,UsersLoginForm
from arch_portal.domain.models.membre import Membre


def subscribe(request):
    if request.method == "POST":
        form = MembreForm(request.POST)
        if form.is_valid():
             user = form.save()
        return redirect("login")
    else:
        form = MembreForm()
    return render(request, "usercore/subscribe.html", {"form":form})   

def log_out(request):
    del request.session["username"]
    del request.session["userid"]
    request.session.flush()
    return redirect("login")

def log_user(request):
    if request.method == "POST":
        form = UsersLoginForm(request.POST)

        if form.is_valid():
            # user = Membre.objects.get(login=form.cleaned_data["login"],pwd = compute_sha1(form.cleaned_data["pwd"]) )
            # if user:
            if user := Membre.objects.get(
                login=form.cleaned_data["login"],
                pwd=compute_sha1(form.cleaned_data["pwd"]),
            ):
                request.session["username"] = user.login 
                request.session["userid"] = user.id
                request.session.modified = True
                return redirect("home" )

    else:
        request.session.get("username1","")
        request.session.get("userid1",0) 
        form = UsersLoginForm()
 
    return render(request, "usercore/login.html", {"form":form})

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

