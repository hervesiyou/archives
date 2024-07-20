from django.shortcuts import redirect, render
from libcore.forms.librairie import LibrairieForm
from libcore.forms.livre import LivreForm
from libcore.models.librairie import Librairie
from libcore.models.livre import Livre
from coreapp.core.serializers import *
from coreapp.models import *
 

def listlibs(request):
    libs = Librairie.objects.all()
    return render(request, "libcore/listlibrairies.html", { "librairies" : libs, } )

def listbooks(request, id):
   
    livres = Livre.objects.filter(librairies=id)
    lib = Librairie.objects.get(id=id)
    serializer = LibrairiesSerializer(lib,many=True)
    # request.session['librairie'] = serializer.data
    request.session['librairie'] = lib.nom
    
    return render(request, "libcore/listbooks.html", { "livres":livres, "librairie" : lib } )


def show_book(request,id):
    liv = Livre.objects.get(id=id)
    return render(request, "libcore/showbook.html", {"livre" : liv} )

def add_book(request):
    librairie = request.session.get('librairie',"")
    if request.method == "POST":
        form = LivreForm(request.POST)
        if form.is_valid():  
            com = form.save() 
            com.save()
            
        return redirect("show_book",com.id )
    else:
        form = LivreForm()
    return render(request, "libcore/addbook.html", {"librairie" : librairie, "form":form} )

def show_librairie(request,id):
    pass

def add_librairie(request):
    
    if request.method == "POST":
        form = LibrairieForm(request.POST)
        if form.is_valid():  
            com = form.save() 
            com.save()
            
        return redirect("show_librairie",com.id )
    else:
        form = LibrairieForm()

    return render(request, "libcore/new_librairie.html", { "form":form  })
