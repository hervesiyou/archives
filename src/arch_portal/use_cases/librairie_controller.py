import json
import datetime
from django.http import JsonResponse
from django.shortcuts import redirect, render
from arch_portal.domain.forms.librairie import LibrairieForm
from arch_portal.domain.forms.livre import LivreForm, ImageFormSet
from arch_portal.domain.models.librairie import Librairie
from arch_portal.domain.models.image import Image
from arch_portal.domain.models.livre import Livre
from arch_portal.domain.models.plantarifaire import Plan
from arch_portal.domain.models.membre import Membre
from arch_portal.domain.models.commandelivre import CommandeLivre
from arch_portal.domain.models.serializers import *
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from arch_portal.use_cases.services.core import send_email
import threading

def show_commandes(request):
    coms = CommandeLivre.objects.all()
    print(f"{coms} total")
    return render(request, "usercore/home.html", { "commandes" : coms} )

def listlibs(request):
    libs = Librairie.objects.all()
    return render(request, "libcore/listlibrairies.html", { "librairies" : libs, } )

def listbooks(request, id,mode=False):
    livres = Livre.objects.filter(librairies=id)
    lib = Librairie.objects.get(id=id)
    serializer = LibrairiesSerializer(lib,many=True) 
    request.session['librairie'] = lib.nom
    request.session['librairieid'] = lib.id
    if( not mode ):
        return render(request, "libcore/listbooks_tab.html", { "livres":livres, "librairie" : lib } )

    return render(request, "libcore/listbooks.html", { "livres":livres, "librairie" : lib } )

def show_book(request,id):
    liv = Livre.objects.get(id=id)
    librairieid = request.session.get('librairieid',"")
    abos=achat=connecte=False
    userid = request.session.get("userid","")
    if( isinstance(userid, int) and userid !="" ):
        user = Membre.objects.get(id=userid)
        abos = user.abonnements.all()
        for a in abos :
            if a.is_active and a.plan.appli == "LIB":
                achat = True
        
        connecte = True
    
    if librairieid is None:
        messages.error(request, "La librairie de ce livre n'existe pas , merci de choisir la librairie de ce livre .")
        return  redirect("listlibs")
    
    return render(request, "libcore/showbook.html", {"livre" : liv,"librairie" : Librairie.objects.get(id=librairieid), "connecte":connecte, "abonnements":abos , "achat":achat} )

def add_book(request):
    librairie = request.session.get('librairie',"")
    librairieid = request.session.get('librairieid',"")
    if librairie is None or librairieid is None:
        messages.error(request, "La librairie correspondante n'existe pas , merci de choisir la librairie de ce livre .")
        return  redirect("listlibs")
    
    if request.method == "POST":
        form = LivreForm(request.POST, request.FILES)
        image_formset = ImageFormSet(request.POST, request.FILES) 
        if form.is_valid(): 
            livre = form.save(commit=False)
            if( livre.type == "Numerique"):
                livre.stock = 1000

            # print(form, livre)
            livre.librairies.add(Librairie.objects.get(id=librairieid)) 
            livre.save()

            if image_formset.is_valid():
                
                for image_form in image_formset:
                    if image_form.has_changed(): 
                        image = image_form.save(commit=False)
                        image.livre = livre 
                        image.save()
                        livre.images.add(image) 
            # else:
            #     com = form.save() 
            #     com.librairies.add(Librairie.objects.get(id=librairieid)) 
            #     com.save()
            return redirect("show_book",livre.id )
        else:
            messages.error(request, f"Veuillez corriger les erreurs suivantes.{form.errors}") 
    else:
        form = LivreForm()
        image_formset = ImageFormSet(queryset=Image.objects.none())  

    return render(request, "libcore/addbook.html", {"librairie" : librairie, "form":form, 'image_formset': image_formset,} )

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

def abonement_librairie(request): 
    plans = Plan.objects.filter(appli="LIB")
    return render(request, "libcore/abonement.html", {"plans" : plans} )


@csrf_exempt
def api_add_order(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax :
        if request.method == "POST" :
            data = json.loads(request.body.decode('utf-8'))
            # print(data,data.get('livre'))
            if data.get('livre') is None:
                return JsonResponse({'status': False ,"message": "Livre incorrect"})
            
            if data.get("possesseur") is None:
                return JsonResponse({'status': False ,"message": "Proprietaire incorrect"})
            
            proprietaire=Membre.objects.get(id=data.get("possesseur"))
            livre=Livre.objects.get(id=data.get("livre"))


            com,already = CommandeLivre.objects.get_or_create(
                nom=data.get("nom"),
                telephone=data.get("telephone"),
                livre=livre,
                # date=datetime.datetime.now(),
                proprietaire=proprietaire, 
                message=data.get("message"),
            )
            # print( already )
            if already:
                com.save()
                # envoi du mail au propriotaire
                sujet = f'Commande de {livre.nom} par {proprietaire.nomcomplet} '
                message = f' {proprietaire.nomcomplet} à commandé {livre.nom}'
                destinataires = [proprietaire.email, "hervesiyou@gmail.com"]

                # t = threading.Thread(target=send_email, args=(sujet, message,  [destinataires]))
                # t.start()
                # send_email(sujet, message, destinataires )
                return JsonResponse({'status':True,"message":f"{com.id}  ajouté avec success"})
            else:
                # print( com, livre.nom)
                return JsonResponse({'status': False, "message": f"Vous avez dejà commandé {livre.nom} "})

        return JsonResponse({"status":False, 'message': 'Invalid request'}, status=400)

    return JsonResponse({"status":False,'message': is_ajax })
    