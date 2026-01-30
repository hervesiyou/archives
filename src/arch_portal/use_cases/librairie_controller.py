import json
# import datetime
from django.http import JsonResponse, HttpResponseForbidden, FileResponse, HttpResponse
# from django.shortcuts import redirect, render
from arch_portal.domain.forms.librairie import LibrairieForm
from arch_portal.domain.forms.livre import LivreForm, ImageFormSet
from arch_portal.domain.models.librairie import Librairie
from arch_portal.domain.models.image import Image
from arch_portal.domain.models.wallet import Wallet
from arch_portal.domain.models.livre import Livre
from arch_portal.domain.models.plantarifaire import Plan
from arch_portal.domain.models.membre import Membre
from arch_portal.domain.models.commandelivre import CommandeLivre
from arch_portal.domain.models.paiementlivre import PaiementLivre
from arch_portal.domain.models.notationlivre import NotationLivre
from arch_portal.domain.models.serializers import *

from django.utils import timezone
from django.utils.crypto import get_random_string

from django.db.models import Q
from django.db import transaction
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from arch_portal.use_cases.services.core import send_email
import threading
import uuid
import os
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404 


import qrcode
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader  

COMMISSION_LIBRAIRIE = 0.10  # 10% de commission sur chaque vente de livre
def show_commandes(request):

    userid = request.session.get("userid","")
    if not userid:
        return redirect("login")
    coms = CommandeLivre.objects.filter(proprietaire=userid)
    # print(f"{coms} total")
    return render(request, "usercore/home.html", { "commandes" : coms} )

def faq(request):
    return render(request, "libcore/faq.html", {} )
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

@transaction.atomic
def payer_livre(request, livre_id):

    if not request.session.get("userid"):
        messages.error(request, "Vous devez être connecté pour effectuer un paiement.")
        return redirect("login")

    # Vérifier si le livre a déjà été payé
    user = get_object_or_404(Membre, id=request.session["userid"])
    livre = get_object_or_404(Livre, id=livre_id)
    paiement_existant = PaiementLivre.objects.filter(  acheteur=user, livre=livre ).first()

    if paiement_existant:
        messages.warning( request,  "Vous avez déjà payé ce livre."        )
        return redirect("show_book", id=livre.id)

    if request.method == "POST":
        """
        ici je dois reconcevoir le paiement pour debiter le portefeuille de l'utilisateur et crediter le portefeuille du proprietaire du livre
        ou celui de richbook si le proprietaire n'a pas de portefeuille, en coupant les frais de service de richbook
        """
        wallet_acheteur = user.wallet
        ancien_proprietaire = livre.proprietaire
        wallet_vendeur = None

        if livre.proprietaire and hasattr(livre.proprietaire, 'wallet'):
            wallet_vendeur = livre.proprietaire.wallet
        else:
            wallet_vendeur = Wallet.objects.get(code="WALL-RICHBOOK")  
        
        if  livre.prix <= 1:
            messages.error( request, f"Ce document n'est pas en vente. Le prix du livre est de {livre.prix} XAF." )
            return redirect("show_book", id=livre.id)
        
        if wallet_acheteur.solde < (livre.prix + livre.prix * COMMISSION_LIBRAIRIE) :
            messages.error( request, f"Le montant de votre compte est insuffisant. Le prix du livre est de {livre.prix} XAF." )
            return redirect("show_book", id=livre.id) 
       
        else:
            # print("Paiement en cours...")
            # Wallet plateforme
            wallet_plateforme = Wallet.objects.get(code="WALL-RICHBOOK")
            if  wallet_plateforme is None:
                messages.error( request, f"Le portefeuille de la plateforme est introuvable." )
                return redirect("show_book", id=livre.id)
            # Crédit plateforme
            commission = livre.prix * COMMISSION_LIBRAIRIE
            wallet_plateforme.solde += int( commission ) 
            wallet_plateforme.save()
            # Crédit proprietaire
            montant_net = livre.prix - commission
            # Débit acheteur
            wallet_acheteur.solde -= int(montant_net + commission)
            wallet_acheteur.save()

            wallet_vendeur.solde += int(montant_net)
            wallet_vendeur.save()
                
            # Transfert de propriété du livre
            livre.proprietaire = user
            livre.save()

            if ancien_proprietaire:
                livre.anciens_proprietaires.add(ancien_proprietaire)
                livre.save()
            
            PaiementLivre.objects.create(  acheteur=user,livre=livre, recepteur=ancien_proprietaire, montant=livre.prix, reference=f"Pay-{livre.id}-{str(uuid.uuid4())}", commission=commission, statut ="PAYE" )
            messages.success( request, "Paiement effectué avec succès. Vous pouvez accéder au livre dès que le gestionnaire de la librairie finalisera votre achat .")

            sujet = f'Commande de {livre.nom} par {user.nomcomplet} '
            message = f' {user.nomcomplet} à commandé le livre <b>{livre.nom}</b> par le prix de {livre.prix} XAF.<br> Veuillez contacter le proprietaire {livre.nom}'
            destinataires = [user.email, settings.EMAIL_HOST_SERVICE, "hervesiyou@gmail.com"]
            # recuperation des mails des administrateurs de la librairie
            for admin in livre.librairies.all():
                destinataires.append( admin.possesseur.email )

            t = threading.Thread(target=send_email, args=(sujet, message,  destinataires))
            t.start()
            return redirect("show_book", id=livre.id)
            
                      

    return render(request, "paiement/payer_livre.html", { "livre": livre })

@transaction.atomic
def rembourser_paiement(request, paiement_id):

    paiement = get_object_or_404(PaiementLivre, id=paiement_id)
    if paiement.statut != "PAYE":
        messages.error(request, "Ce paiement ne peut pas être remboursé.")
        return redirect("historique_paiements")

    acheteur = paiement.acheteur
    vendeur = paiement.recepteur
    livre = paiement.livre

    montant = paiement.montant
    commission = paiement.commission
    montant_net = montant - commission
    wallet_plateforme = Wallet.objects.get(code="WALL-RICHBOOK")

    # 🔻 Vérifications de sécurité
    if vendeur and vendeur.wallet.solde < montant_net:
        # raise Exception("Solde vendeur insuffisant pour remboursement")
        messages.error(request, "Solde vendeur insuffisant pour remboursement.")
        return redirect("historique_paiements")

    if wallet_plateforme.solde < commission:
        # raise Exception("Solde plateforme insuffisant")
        messages.error(request, "Solde plateforme insuffisant pour remboursement.")
        return redirect("historique_paiements")

    # 🔻 Débit vendeur
    if vendeur:
        wallet_vendeur = vendeur.wallet
        wallet_vendeur.solde -= montant_net
        wallet_vendeur.save()

    # 🔻 Débit plateforme
    wallet_plateforme.solde -= commission
    wallet_plateforme.save()

    # 🔺 Crédit acheteur
    wallet_acheteur = acheteur.wallet
    wallet_acheteur.solde += montant
    wallet_acheteur.save()

    # 🔁 Restaurer la propriété du livre
    anciens = livre.anciens_proprietaires.all()
    ancien_proprio = anciens.last() if anciens.exists() else None

    if ancien_proprio:
        livre.proprietaire = ancien_proprio
        livre.anciens_proprietaires.remove(ancien_proprio)
    else:
        livre.proprietaire = None

    livre.save()

    # 🧾 Mise à jour paiement
    paiement.statut = "REMBOURSE"
    paiement.date_remboursement = timezone.now()
    paiement.reference_remboursement = f"REF-{get_random_string(12)}"
    paiement.save()

    return paiement

def historique_paiements(request):
    if not request.session.get("userid"):
        return redirect("login")

    user = get_object_or_404(Membre, id=request.session["userid"])
    paiements = PaiementLivre.objects.filter(acheteur=user)
    return render(request, "libcore/historiquepaiement.html", { "paiements": paiements, "user": user })

def verifier_facture(request, reference):
    paiement = get_object_or_404(PaiementLivre, reference=reference)
    return render(request, "libcore/verifier.html", {"paiement": paiement})


def facture_pdf(request, paiement_id):
    if not request.session.get("userid"):
        return redirect("login")

    paiement = get_object_or_404(PaiementLivre, id=paiement_id)
    # Sécurité : seul l'acheteur peut accéder
    if paiement.acheteur.id != request.session["userid"]:
        return HttpResponseForbidden("Accès interdit")

    logo_path = os.path.join(settings.BASE_DIR, "arch_portal/static/images/logo.png")
    logo = ImageReader(logo_path)
    
    qr_data = (
        f"FACTURE DE PAIEMENT de livre \n"
        f"Reference: {paiement.reference}\n"
        f"Acheteur: {paiement.acheteur.nomcomplet}\n"
        f"Livre: {paiement.livre.nom}\n"
        f"Montant: {paiement.montant} XAF\n"
        f"Date: {paiement.date_paiement.strftime('%d/%m/%Y %H:%M')}"
        f"https://{settings.URL_SITE}/fac/verif/{paiement.reference}"

    )

    qr_img = qrcode.make(qr_data)
    buffer = BytesIO()
    qr_img.save(buffer, format="PNG")
    buffer.seek(0)
    qr_reader = ImageReader(buffer)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = ( f'attachment; filename="facture_{paiement.reference}.pdf"' )

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    # LOGO
    p.drawImage(
        logo,
        140,
        height - 100,
        width=120,
        height=100,
        preserveAspectRatio=True,
        mask='auto'
    )

    # TITRE
    p.setFont("Helvetica-Bold", 18)
    p.drawString(50, height - 50, "FACTURE DE PAIEMENT - RichBook Archives")

    # INFOS FACTURE
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 100, f"Référence : {paiement.reference}")
    p.drawString(50, height - 130, f"Acheteur : {paiement.acheteur.nomcomplet}")
    p.drawString(50, height - 160, f"Livre : {paiement.livre.nom}")
    p.drawString(50, height - 190, f"Montant : {paiement.montant} XAF")
    p.drawString(
        50,
        height - 220,
        f"Date : {paiement.date_paiement.strftime('%d/%m/%Y %H:%M')}"
    )

    # QR CODE (en bas à droite)
    p.drawImage(
        qr_reader,
        width - 180,
        50,
        width=120,
        height=120
    )

    p.setFont("Helvetica-Oblique", 10)
    p.drawString(
        width - 180,
        40,
        "Scanner pour vérifier la facture"
    )

    # FOOTER
    p.setFont("Helvetica", 11)
    p.drawString(50, 50, "Merci pour votre confiance et votre soutien à RichBook Archives.")

    p.showPage()
    p.save()

    return response


def show_book(request,id):
    liv = Livre.objects.get(id=id)
    librairieid = request.session.get('librairieid',"")
    abos = achat=connecte=False
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
            livre = form.save(commit=True)
            # livre = form.save(commit=False)
            if( livre.type == "Numerique"):
                livre.stock = 1000

            # print(form, livre)
            # livre.librairies.add(Librairie.objects.get(id=librairieid)) 
            # livre.save()
            try:
                librairie = Librairie.objects.filter(id=librairieid).first()
                if librairie:
                    livre.librairies.add(librairie)
                    livre.save()
            
            except Librairie.DoesNotExist:
                print("Librairie introuvable")

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

def show_book_file(request,id):
     
    if not request.session.get("userid"):
        messages.error(request, "Vous devez être connecté.")
        return redirect("login")

    user = get_object_or_404(Membre, id=request.session["userid"])
    livre = get_object_or_404(Livre, id=id)
    # Vérifier paiement
    paiement = PaiementLivre.objects.filter(   acheteur=user, livre=livre ).first()

    if not paiement and livre.prix > 0:
        return HttpResponseForbidden("Vous n'avez pas payé ce livre.")

    # return FileResponse(  livre.file.open(), as_attachment=True,  filename=livre.file.name  )
    else: 
        # livre = Livre.objects.get(id=id)
        if livre:
            return render(request, "libcore/showbookfile.html", {"livre" : livre, } )
        else:
            print("Erreur lors du chargement du livre ")
        #    return redirect("show_book",livre.id ) 

def search_book(request):
    name = request.POST.get("rechLivre","")
    print(name) 
    livres = Livre.objects.filter(
        Q(nom__icontains=name) |
        Q(auteur__icontains=name) | 
        Q(description__icontains=name)|
        Q(domaine__icontains=name)
    )
    # if livres.exists():
    return render(request, "libcore/listsearchedbooks.html", { "livres":livres , "name": name} )
    # else:
        # print("erreur lors de la recherche du livre ")
        #  return redirect("show_book",livre.id ) 

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
 

def noter_livre(request, livre_id):
    if not request.session.get("userid"):
        messages.error(request, "Veuillez vous connecter pour noter ce livre.")
        return redirect("login")

    user = get_object_or_404(Membre, id=request.session["userid"])
    livre = get_object_or_404(Livre, id=livre_id)

    # Vérifier si déjà noté
    if NotationLivre.objects.filter(livre=livre, auteur=user).exists():
        messages.warning(request, "Vous avez déjà noté ce livre.")
        return redirect("show_book", id=livre.id)

    if request.method == "POST":
        note = int(request.POST.get("note"))
        commentaire = request.POST.get("commentaire", "")

        if note < 1 or note > 5:
            messages.error(request, "La note doit être entre 1 et 5 étoiles.")
            return redirect("show_book", id=livre.id)

        NotationLivre.objects.create(  livre=livre,  auteur=user,  note=note,  commentaire=commentaire  )
        messages.success(request, "Merci pour votre note ⭐")
        return redirect("show_book", id=livre.id)

    return redirect("show_book", id=livre.id)


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
                destinataires = [proprietaire.email, settings.EMAIL_HOST_SERVICE ,"hervesiyou@gmail.com"]

                t = threading.Thread(target=send_email, args=(sujet, message,  destinataires ))
                t.start()
                # send_email(sujet, message, destinataires )
                return JsonResponse({'status':True,"message":f"{com.id}  ajouté avec success"})
            else:
                # print( com, livre.nom)
                return JsonResponse({'status': False, "message": f"Vous avez dejà commandé {livre.nom} "})

        return JsonResponse({"status":False, 'message': 'Invalid request'}, status=400)

    return JsonResponse({"status":False,'message': is_ajax })
    