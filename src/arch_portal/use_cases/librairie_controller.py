import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from arch_portal.domain.forms.librairie import LibrairieForm
from arch_portal.domain.forms.livre import LivreForm
from arch_portal.domain.models.librairie import Librairie
from arch_portal.domain.models.livre import Livre
from arch_portal.domain.models.membre import Membre
from arch_portal.domain.models.commandelivre import CommandeLivre
from arch_portal.domain.models.serializers import *
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

def listlibs(request):
    libs = Librairie.objects.all()
    return render(request, "libcore/listlibrairies.html", { "librairies" : libs, } )

def listbooks(request, id):
    livres = Livre.objects.filter(librairies=id)
    lib = Librairie.objects.get(id=id)
    serializer = LibrairiesSerializer(lib,many=True) 
    request.session['librairie'] = lib.nom
    request.session['librairieid'] = lib.id
    
    return render(request, "libcore/listbooks.html", { "livres":livres, "librairie" : lib } )

def show_book(request,id):
    liv = Livre.objects.get(id=id)
    librairieid = request.session.get('librairieid',"")
    
    if librairieid is None:
        messages.error(request, "La librairie de ce livre n'existe pas , merci de choisir la librairie de ce livre .")
        return  redirect("listlibs")
    
    return render(request, "libcore/showbook.html", {"livre" : liv,"librairie" : Librairie.objects.get(id=librairieid)} )

def add_book(request):
    librairie = request.session.get('librairie',"")
    librairieid = request.session.get('librairieid',"")
    if librairie is None or librairieid is None:
        messages.error(request, "La librairie correspondante n'existe pas , merci de choisir la librairie de ce livre .")
        return  redirect("listlibs")
    
    if request.method == "POST":
        form = LivreForm(request.POST)
        if form.is_valid():  
            com = form.save() 
            com.librairies.add(Librairie.objects.get(id=librairieid)) 
            com.save()
            return redirect("show_book",com.id )
        else:
            messages.error(request, f"Veuillez corriger les erreurs suivantes.{form.errors}") 
    else:
        form = LivreForm()
    return render(request, "libcore/addbook.html", {"librairie" : librairie, "form":form} )

def show_librairie(request,id):
    lib = Librairie.objects.get(id=id)
    return render(request, "libcore/show_librairie.html", { "librairie" : lib, } )

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

@csrf_exempt
def api_add_order(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax :
        if request.method == "POST" :
            data = json.loads(request.body.decode('utf-8'))
            print(data,data.get('livre'))
            if data.get('livre') is None:
                return JsonResponse({'status': False ,"message": "Livre incorrect"})
            
            if data.get("possesseur") is None:
                return JsonResponse({'status': False ,"message": "Proprietaire incorrect"})
            
            proprietaire=Membre.objects.get(id=data.get("possesseur"))
            livre=Livre.objects.get(id=data.get("livre"))
            
            com=CommandeLivre.objects.create(
                nom=data.get("nom"),
                telephone=data.get("telephone"),
                livre=livre,
                proprietaire=proprietaire, 
                message=data.get("message"),
            )
            com.save()  

            return JsonResponse({'status':True,"message":f"{com.id}  ajouté avec success"})
        return JsonResponse({"status":False, 'message': 'Invalid request'}, status=400)

    return JsonResponse({"status":False,'message': is_ajax })
    