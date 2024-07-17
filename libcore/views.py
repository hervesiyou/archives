from django.shortcuts import render

from coreapp.models import *
# Create your views here.

def listlibs(request):
    libs = Librairies.objects.all()
 
    return render(request, "libcore/listlibrairies.html", { "librairies" : libs, } )

def listbooks(request, id):
   
    livres = Livres.objects.filter(librairies=id)
    lib = Librairies.objects.get(id=id) 
 
    return render(request, "libcore/listbooks.html", { "livres":livres, "librairie" : lib } )


def show_book(request,id):
    liv = Livres.objects.get(id=id)
    return render(request, "libcore/showbook.html", {"livre" : liv} )
