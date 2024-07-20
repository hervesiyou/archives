from django.shortcuts import redirect, render
from archcore.forms import CommunauteForm,FamilleForm,AssociationForm
from coreapp.models.communaute import Communaute
from coreapp.models.famille import Famille
from coreapp.models import *


def listcom(request):
    communautes = Communaute.objects.all()
    return render(request, "archcore/listcom.html", { "communautes":communautes, })

def listfamilles(request, id):
   
    livres = Famille.objects.filter(communaute=id)
    lib = Communaute.objects.get(id=id) 
    return render(request, "archcore/listfamilles.html", { "familles" : livres, "communaute" : lib } )

def show_famille(request,id):
    liv = Famille.objects.get(id=id)
    print( "membres: {}".format(liv.get_members()) )
    return render(request, "archcore/showfamille.html", {"famille" : liv} )

 
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

def show_association(request,id):
    pass
def add_association(request):
    
    if request.method == "POST":
        form = AssociationForm(request.POST)
        if form.is_valid():  
            com = form.save() 
            com.save()
            
        return redirect("show_association",com.id )
    else:
        form = AssociationForm()

    return render(request, "archcore/new_association.html", { "form":form  })

def show_communaute(request, id):
    pass

def add_communaute(request):
    
    if request.method == "POST":
        form = CommunauteForm(request.POST)
        if form.is_valid():  
            com = form.save() 
            com.save()
            
        return redirect("show_communaute",com.id )
    else:
        form = CommunauteForm()

    return render(request, "archcore/new_communaute.html", { "form":form })

