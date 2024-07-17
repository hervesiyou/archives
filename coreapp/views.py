from django.shortcuts import render, redirect
from coreapp.models import *


# Create your views here.
def index(request): 
    return render(request, "base.html" )

def show_com(request,id):
    com = Communautes.objects.get(id=id)
    return render(request, "show_com.html", {"communaute":com})

def log_out(request):

    del request.session["username"]
    del request.session["userid"]
    request.session.flush()

    return redirect("index")

def log_user(request):
    if request.method == "POST":
        form = UsersLoginForm(request.POST)

        if form.is_valid():
            user = Users.objects.get(login=form.cleaned_data["login"],pwd = compute_sha1(form.cleaned_data["pwd"]) )
            if user:
                request.session["username"] = user.login
                # request.session.get("username1",user.login)
                # request.session.get("userid1",user.id) 
                request.session["userid"] = user.id
                request.session.modified = True
                return redirect("home" )

    else:
        request.session.get("username1","")
        request.session.get("userid1",0) 
        form = UsersLoginForm()
 
    return render(request, "login.html", {"form":form})
