from django.shortcuts import render
from coreapp.models import *
# Create your views here.

def listcom(request):
    communautes = Communautes.objects.all()
    return render(request, "archcore/listcom.html", { "communautes":communautes, })

def listfamilles(request, id):
   
    livres = Familles.objects.filter(communaute=id)
    lib = Communautes.objects.get(id=id) 
    return render(request, "archcore/listfamilles.html", { "familles" : livres, "communaute" : lib } )


def show_famille(request,id):
    liv = Familles.objects.get(id=id)
    print( "membres: {}".format(liv.get_members()))
    return render(request, "archcore/showfamille.html", {"famille" : liv} )