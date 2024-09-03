from django.shortcuts import redirect, render
from arch_portal.domain.forms.galerie import GalerieForm
from arch_portal.domain.forms.association import AssociationForm
from arch_portal.domain.forms.communaute import CommunauteForm 
from arch_portal.domain.models.communaute import Communaute
from arch_portal.domain.models.famille import Famille
from arch_portal.domain.models import *

from arch_portal.domain.models import Association


def listcom(request):
    communautes = Communaute.objects.all()
    return render(request, "archcore/listcom.html", { "communautes":communautes, })

def show_association(request,id):
    asso = Association.objects.get(id=id)
    return render(request, "archcore/showassociation.html", {"association": asso})


def listassociations(request, id):
    assos = Association.objects.filter(communaute=id)
    com = Communaute.objects.get(id=id)
    return render(request, "archcore/listassociations.html", {"associations": assos, "communaute": com})

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
 

def show_communaute(request,id):
    com = Communaute.objects.get(id=id)
    return render(request, "archcore/show_com.html", {"communaute":com})

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
