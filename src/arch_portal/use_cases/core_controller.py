from django.shortcuts import render, redirect ,get_object_or_404
from django.conf import settings
from arch_portal.domain.exceptions.membre_exception import MembreException
from arch_portal.domain.models.salleattentefamille import SalleAttenteFamille
from arch_portal.domain.models.communaute import Communaute
from arch_portal.domain.models.famille import Famille
from arch_portal.domain.models.contact import Contact
from arch_portal.domain.models.membre import Membre
from arch_portal.domain.models.livre import Livre
# from arch_portal.domain.models.image import Image
from arch_portal.domain.models.plantarifaire import Plan
from arch_portal.domain.models.facture import Facture
from arch_portal.domain.models.message import Message
from arch_portal.domain.models.marche import Marche
from arch_portal.domain.models.invitationadminfamille import InvitationAdminFamille
from arch_portal.domain.models.association import Association
from arch_portal.domain.models.librairie import Librairie
from arch_portal.domain.models.librairiemessage import LibrairieMessage
from arch_portal.domain.models.communitymessage import CommunauteMessage
from arch_portal.domain.models.salleattentecommunaute import SalleAttenteCommunaute
from arch_portal.domain.models.salleattentefamillemere import SalleAttenteFamilleMere
from arch_portal.domain.models.salleattenteassociation import SalleAttenteAssociation
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from arch_portal.use_cases.services.subscription_service import get_membre_from_session

from django.db.models import Q

import json
from datetime import date
from arch_portal.use_cases.services.core import send_email
from django.http import HttpResponseForbidden, JsonResponse
from datetime import date, datetime
from django.contrib import messages
from arch_portal.use_cases.services.core import generate_token, send_invitation_adminfamille_mail
from arch_portal.use_cases.services.facture_service import generer_facture_pdf, envoyer_facture_email
from django.urls import reverse
from decimal import Decimal
from django.db import transaction
from django.db.transaction import on_commit
from arch_portal.domain.models.abonnement import Abonnement
from arch_portal.domain.models.transaction import Transaction
import threading

import secrets
from django.shortcuts import render, redirect, get_object_or_404 
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags
from django.conf import settings
from datetime import timedelta 
from arch_portal.domain.forms.membre import DemandeResetPasswordForm, ResetPasswordForm
from arch_portal.use_cases.services.core import compute_sha1

TOKEN_VALIDITY_MINUTES = 30


def demander_reset_password(request):
    """Étape 1 : le membre saisit son email"""
    if request.method == "POST":
        form = DemandeResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            membre = Membre.objects.filter(email=email).first()

            if membre:
                # Génère un token sécurisé et sa date d'expiration
                token = secrets.token_urlsafe(32)
                membre.token = token
                membre.token_expiration = timezone.now() + timedelta(minutes=TOKEN_VALIDITY_MINUTES)
                membre.save(update_fields=['token', 'token_expiration'])

                lien_reset = request.build_absolute_uri(
                    f"/r-password/{membre.id}/{token}/"
                )

                sujet = "Réinitialisation de votre mot de passe"
                html_message = render_to_string("includes/reset_password_email.html", {
                    "membre": membre,
                    "lien_reset": lien_reset,
                    "validite_minutes": TOKEN_VALIDITY_MINUTES,
                })
                message_texte = strip_tags(html_message)

                try:
                    nb_envoyes = send_mail(
                        subject=sujet,
                        message=message_texte,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[email, "hervesiyou@gmail.com"],
                        html_message=html_message,
                        fail_silently=False,
                    )
                    print(f"Emails envoyés : {nb_envoyes}")
                except Exception as e:
                    print(f"Erreur d'envoi d'email : {e}")
                    messages.error(request, f"Erreur lors de l'envoi de l'email : {e}")                
                # messages.error(
                #     request,
                #     message_texte
                # )
                # print(membre)

             
            # Message générique, que l'email existe ou non (évite l'énumération de comptes)
            messages.success(
                request,
                "Si cet email est associé à un compte, un lien de réinitialisation vient de vous être envoyé."
            )
            return redirect("login")
    else:
        form = DemandeResetPasswordForm()

    return render(request, "includes/demander_reset_password.html", {"form": form})


def reset_password(request, membre_id, token):
    """Étape 2 : le membre saisit son ancien + nouveau mot de passe"""
    membre = get_object_or_404(Membre, id=membre_id, token=token)

    # Vérification de l'expiration du token
    if not membre.token_expiration or membre.token_expiration < timezone.now():
        messages.error(request, "Ce lien de réinitialisation a expiré. Merci de refaire une demande.")
        return redirect("demander_reset_password")

    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            ancien_password = form.cleaned_data['ancien_password']
            nouveau_password = form.cleaned_data['nouveau_password']

            if   False:
            # if compute_sha1(ancien_password) != membre.pwd or False:
                form.add_error('ancien_password', f"L'ancien mot de passe est incorrect {compute_sha1(ancien_password)} et {membre.pwd}.")
            else:
                membre.pwd = compute_sha1(nouveau_password)
                # Invalide le token après usage (usage unique)
                membre.token = ""
                membre.token_expiration = None
                membre.save(update_fields=['pwd', 'token', 'token_expiration'])

                messages.success(request, "Votre mot de passe a été modifié avec succès.")
                return redirect("login")
    else:
        form = ResetPasswordForm()

    return render(request, "includes/reset_password.html", {"form": form, "membre": membre})

def about(request):
    # user = get_object_or_404(Membre, id=user_id)
    # abonnements = Abonnement.objects.filter(membre=user, is_active=True) 
    return render(request, "includes/about.html" )

def show_subscriptions(request, user_id):
    user = get_object_or_404(Membre, id=user_id)
    abonnements = Abonnement.objects.filter(membre=user, is_active=True)
    return render(request, "usercore/show_user_abonnements.html", {"abonnements": abonnements, "user": user})

@transaction.atomic
@csrf_exempt
def souscrire_abonnement(request):
    # les plan_appli sont FREE BASIC PRO DIAMOND    
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax :
        if request.method == "POST" :
            data = json.loads(request.body.decode('utf-8'))
            membre = data.get("membre")
            plan = data.get("plan")
            type = data.get("type")

        # Vérifier si le membre a déjà un abonnement actif pour ce plan
        abonnement = Abonnement.objects.filter(membre_id=membre, plan_appli=plan, type=type, is_active=True).first()
        if abonnement:
                response = {
                    "status": False,
                    "message": f"Vous avez déjà un abonnement actif pour le plan {plan}."
                }
                return JsonResponse(response)

        response = {"status": False, "message": "Une erreur est survenue lors de la souscription à l'abonnement."}
        if not membre or not plan:
            # raise ValueError("Membre et plan sont requis pour souscrire à un abonnement.")
            response["message"] = "Membre et plan sont requis pour souscrire à un abonnement.."
            response["status"] = False
            return JsonResponse(response)
        try:
            #  pour le moment les plans sont en dur, mais à terme ils seront dans la base de données et on pourra faire un switch case sur le nom du plan pour appliquer des règles spécifiques à chaque plan
            membre = Membre.objects.get(id=membre)
        except Membre.DoesNotExist:
            # raise MembreException(f"Membre avec id {membre} introuvable.")
            response["message"] = f"Membre avec  {membre} introuvable."
            response["status"] = False
            return JsonResponse(response)
        
        if membre is None:
            # raise MembreException(f"Membre avec id {membre} introuvable.")
            response["message"] = f"Membre avec id {membre} introuvable."
            response["status"] = False
            return JsonResponse(response)  
        
        if plan == "FREE":
            prix = 0 
            p = Plan.objects.create(
                nom = f"PL-{type}-{plan}-{membre.login}",
                nbcommunautes = 0,
                nbadministrateurs = 0,
                nbfamilles = 1,
                nblivres = 0,
                nbcagnotes = 1,
                nblibrairies = 0,
                prix = prix
            )
        
        elif plan == "BASIC":
            prix = 19000  
            p = Plan.objects.create(
                nom = f"PL-{type}-{plan}-{membre.login}",
                nbcommunautes = 1,
                nbadministrateurs = 5,
                nbfamilles = 10,
                nblivres = 0,
                nbcagnotes = 3,
                nblibrairies = 0,

                nbassociations = 1,
                nbprojets = 1,
                nbevenements = 1,

                prix = prix
            ) 
            
        elif plan == "PRO":
            prix = 29000
            p = Plan.objects.create(
                nom = f"PL-{type}-{plan}-{membre.login}",
                nbcommunautes = 2,
                nbadministrateurs = 10,
                nbfamilles = 20,
                nblivres = 0,
                nbcagnotes = 6,
                nblibrairies = 0,

                nbassociations=5,
                nbprojets = 3,
                nbevenements = 5,

                prix = prix
            ) 
            
        elif plan == "DIAMOND":
            prix = 50000
            p = Plan.objects.create(
                nom = f"PL-{type}-{plan}-{membre.login}",
                nbcommunautes = 5,
                nbadministrateurs = 15,
                nbfamilles = 50,
                nblivres = 0,
                nbcagnotes = 10,
                nblibrairies = 0,

                nbassociations=10,
                nbprojets = 10,
                nbevenements = 10,

                prix = prix
            )
             
        elif plan =="FREEREADER":
            prix = 7000
            p = Plan.objects.create(
                nom = f"PL-{type}-{plan}-{membre.login}",
                nbcommunautes = 0,
                nbadministrateurs = 0,
                nbfamilles = 0,
                nblivres = 0,
                nbcagnotes = 0,
                nblibrairies = 0,
                prix = prix
            )

        elif plan == "PROREADER":
            prix = 12000
            p = Plan.objects.create(
                nom = f"PL-{type}-{plan}-{membre.login}",
                nbcommunautes = 0,
                nbadministrateurs = 0,
                nbfamilles = 0,
                nblivres = 0,
                nbcagnotes = 0,
                nblibrairies = 0,
                prix = prix
            )

        elif plan == "PROLIBRAIRE":
            prix = 29000 
            p = Plan.objects.create(
                nom = f"PL-{type}-{plan}-{membre.login}",
                nbcommunautes = 0,
                nbadministrateurs = 0,
                nbfamilles = 0,
                nblivres = 100,
                nbcagnotes = 0,
                nblibrairies = 1,
                prix = prix
            )      
            
        wallet = membre.wallet
        if wallet.solde < prix:
            response["message"] = "Solde insuffisant pour souscrire à ce plan d'abonnement."
            response["status"] = False
            return JsonResponse(response)
        
        # je cree l'abonnement correspondant 
        abonnement = Abonnement.objects.create(
            membre=membre,
            plan = p,
            debut=date.today(),
            plan_appli=plan,
            prix=prix,
            type=type,
            is_active=True,
            duree=365
        )

        wallet.solde -= Decimal(prix)
        wallet.save() 
        abonnement.save()

        transaction_paiement =  Transaction.objects.create(
            code=f"TRX-ABO-{abonnement.id}",
            wallet=wallet,
            montant=Decimal(prix),
            type="ABONNEMENT",
            status="SUCCESS",
            description=f"Abonnement au plan {abonnement.plan_appli} pour le membre {membre.nomcomplet}"
        )

        facture = Facture.objects.create(
            membre=membre,
            abonnement=abonnement,
            transaction=transaction_paiement,
            montant=Decimal(prix),
            devise="XAF",
            status="PAYEE"
        )

        def traiter_facture():
            try:
                facture.refresh_from_db()
                generer_facture_pdf(facture)
                envoyer_facture_email(facture)

            except Exception as e:
                print( f"Erreur facture {facture.numero} : {str(e)}" )
                
        transaction.on_commit(traiter_facture)

        response["status"] = True
        response["message"] = "Abonnement souscrit avec succès."
        return JsonResponse(response)

    return HttpResponseForbidden()

def temoignages(request): 
    testimonials = [ 
        {
        'name': "Dr. Marie-Claire Fotso",
        'location': "Yaoundé, Cameroun",
        'avatar': "images/users/f4.png", 
        'quote': "Richbook m’a permis de redécouvrir l’histoire complète de ma chefferie Bameka. C’est bien plus qu’une plateforme, c’est un pont entre nos racines et l’avenir."
      },
      {
        'name': "Jean-Pierre Nguetchueng",
        'location': "Douala, Cameroun",
        'avatar': "images/users/h3.png",
        'quote': "Grâce à la librairie digitale, j’ai pu former toute mon équipe au marketing digital sans dépenser une fortune. Le contenu est de très haute qualité."
      },
      {
        'name': "Aïcha Djomo",
        'location': "Paris, France (Diaspora)",
        'avatar': "images/users/h4.png",
        'quote': "Enfin un espace qui valorise notre patrimoine bamiléké tout en nous donnant des outils concrets pour réussir. Je me sens fière et outillée."
      },
      {
        'name': "Chef Honoré Tchoupo",
        'location': "Bandjoun",
        'avatar': "images/users/h2.png",
        'quote': "Richbook archive dignement notre histoire. Mes enfants et petits-enfants peuvent maintenant apprendre notre passé sans voyager."
      },
      {
        'name': "Stéphane Mbal",
        'location': "Bafoussam",
        'avatar': "images/users/7.jpg",
        'quote': "Les livres sur le hacking éthique et la cybersécurité m’ont ouvert les yeux. Je recommande fortement à tous les jeunes camerounais."
      },
      {
        'name': "Fatou Bakary",
        'location': "Yaoundé",
        'avatar': "images/users/h1.png",
        'quote': "Le slider des archives communautaires est magnifique. J’ai passé des heures à découvrir des quartiers et chefferies que je ne connaissais pas."
      },
      {
        'name': "Olivier Kemajou",
        'location': "Montréal, Canada",
        'avatar': "images/users/f3.png",
        'quote': "En tant que membre de la diaspora, Richbook me reconnecte à mes origines tout en m’aidant à développer mes compétences professionnelles."
      },
      {
        'name': "Pr. Élisabeth Wambo",
        'location': "Dschang",
        'avatar': "images/users/f2.png",
        'quote': "Une initiative remarquable qui allie préservation du patrimoine et développement personnel. Bravo à l’équipe !"
      },
      {
        'name': "Armel Takougang",
        'location': "Buea",
        'avatar': "images/users/f1.png",
        'quote': "J’ai trouvé dans la section Budo Masters des connaissances qui m’ont aidé à progresser en arts martiaux avec une vraie dimension culturelle."
      },
      {
        'name': "Sophie Nkoumou",
        'location': "Berlin, Allemagne",
        'avatar': "images/users/f5.png",
        'quote': "Richbook est devenu mon rituel du dimanche. Je lis, j’apprends, je m’inspire. Merci pour ce beau projet panafricain."
      }
    ]

    return render(request,"includes/temoignages.html", { "temoignages" : testimonials})

 
def index(request): 
    coms = Communaute.objects.all()
    livres = Livre.objects.all()
    librairies = Librairie.objects.all()
    marches = Marche.objects.all()
    membres = Membre.objects.all()

    return render(request, "base.html",
        {
            "nbcommunautes" : len(coms),
            "nblivres": len(livres),
            "nblibrairies" : len(librairies),
            "nbmarches": len(marches),
            "nbmembres": len(membres),
        } )

def contact(request): 

    if request.method == "POST":
        # traitement du formulaire
        name = request.POST.get("name")
        email = request.POST.get("email") 
        message = request.POST.get("message")
        
        if (name and  email and  message) :
            contact = Contact.objects.filter(email=email, sender=name, message=message).first()
            if contact is not None:
                messages.info(request, "Vous avez déjà envoyé ce message. Merci de votre compréhension.")
                return redirect("index")
            
            contact = Contact(sender=name, email=email, message=message)
            contact.save()
            messages.success(request, "Votre message a bien été envoyé. Merci !")
            send_email("Contact par " + email+ " - " + name + " :", message, [email, settings.EMAIL_HOST_USER,"mfrelyon@gmail.com"])
            # ici tu peux sauvegarder le message ou l'envoyer par email
            return redirect("index")  

    return render(request, "includes/contact.html", {
        # "HCAPTCHA": getattr(settings, "APP_HCAPTCHA", None),
        # "ORANGE": getattr(settings, "NO_ORANGE", None),
        # "MTN": getattr(settings, "NO_MTN", None),
        # "SARA": getattr(settings, "NO_SARA", None),
        # "VERSION": "1.0.1"
    })
    # return render(request, "includes/contact.html" )

def show_com_salle(request,id):
    user = get_membre_from_session(request)
# if(request.session["userid"]!=None):
    # user = Membre.objects.get(id=request.session["userid"])
    if(user != None):
        com = Communaute.objects.get(id=id)

        users = SalleAttenteCommunaute.objects.filter(communaute=com)
        return render(request, "usercore/salleattentecom.html", { "communaute": com, "users":users,"user":user})
    else:
        # raise MembreException( f" Membre {request.session['userid']} introuvable ")  
        return redirect(f"{reverse('login')}?next={request.get_full_path()}")
    # else:
        # return redirect("login")

def show_fam_salle_fusion(request,id):
    user = get_membre_from_session(request) 
    if(user != None):
        com = Famille.objects.get(id=id)
        salles = SalleAttenteFamilleMere.objects.filter(famille=com)
        return render(request, "usercore/salleattentefammere.html", { 
            "famille": com, 
            "sallesattentes":salles, 
            # "famillemere":com.famille_mere,
            "user":user
        })
    else:
        # raise MembreException( f" Membre {request.session['userid']} introuvable ")  
        return redirect(f"{reverse('login')}?next={request.get_full_path()}")
    # else:
        # return redirect("login")

def show_fam_salle(request,id):
    user = get_membre_from_session(request)
    # if(request.session["userid"]!=None):
    # user = Membre.objects.get(id=request.session["userid"])
    if(user != None):
        com = Famille.objects.get(id=id)
        users = SalleAttenteFamille.objects.filter(famille=com)
        return render(request, "usercore/salleattentefam.html", { "famille": com, "users":users, "user":user})
    else:
        # raise MembreException( f" Membre {request.session['userid']} introuvable ")  
        return redirect(f"{reverse('login')}?next={request.get_full_path()}")
  
def show_asso_salle(request,id):
    user = get_membre_from_session(request)

    # if(request.session["userid"]!=None):
    user = Membre.objects.get(id=request.session["userid"])
    if(user != None):
        com = Association.objects.get(id=id)

        users = SalleAttenteAssociation.objects.filter(association=com)
        return render(request, "usercore/salleattenteasso.html", { "association": com, "users":users, "user":user})
    else:
        # raise MembreException( f" Membre {request.session['userid']} introuvable ") 
        return redirect(f"{reverse('login')}?next={request.get_full_path()}") 

def admin_accept_invitation(request,token):
    
    inv = InvitationAdminFamille.objects.filter(token=token).first()

    if not inv :
        messages.error(request, "Cette invitation n'existe pas ou a expiré.")
        return redirect('index')
    
    if hasattr(inv, 'etat') and inv.etat and "Validé" in str(inv.etat):
        messages.warning(request, "Cette invitation a déjà été acceptée.")
        return redirect('show_famille', id=inv.famille.id)
    
    membre = Membre.objects.filter(email=inv.email).first()
    inv.famille.administrateurs.add(membre)
    inv.famille.membres_famille.add(membre)
    inv.emetteur.familles.add(inv.famille)
    inv.datevalidation = datetime.now()
    inv.etat =f" Validé le {0}".format(inv.datevalidation)
    # inv.famille.save()
    # inv.emetteur.save()
    messages.success(request,f" Bravo, vous avez accepté l'invitation de  { inv.nomcomplet} à administrer { inv.famille.nom }  !")

    return redirect('show_famille', id=inv.famille.id)

def admin_create(request,id):

    famille = get_object_or_404(Famille,pk=id)
    userid = request.session.get("userid","") 
    membre = get_object_or_404(Membre,pk=userid)

    if not(membre in famille.administrateurs.all()):
        messages.danger(request,f" Desolé, vous n'avez pas le droit d'administrer { famille.nom }  !")
    else:
        if request.method == "POST":  

            if userid :
                
                nom = request.POST.get('nom')
                email = request.POST.get('email')
                message = request.POST.get('message')

                if( InvitationAdminFamille.objects.filter(nomcomplet=nom, emetteur=membre,famille=famille).exists()):
                    messages.error(request,f" Desolé, vous avez déjà invité  { nom} à administrer { famille.nom }  !")
                    return redirect("edit_famille", id=famille.id )
                
                # je genere le token et je cree l'invitaition 
                token = generate_token(nom)

                inv = InvitationAdminFamille(
                    nomcomplet = nom,
                    famille=famille,
                    emetteur = membre,
                    email = email,
                    message= message,
                    token=token.replace(" ", ""),
                )

                # send_invitation_adminfamille_mail(
                #     email=email,
                #     token=token,
                #     nomfamille=famille.nom, 
                #     emnom=membre.nomcomplet,
                #     nom=nom,
                #     message=message
                # )

                thread = threading.Thread(
                    target=send_invitation_adminfamille_mail, 
                    args=(email, token, famille.nom, membre.nomcomplet,nom,message)
                )
                thread.daemon = True
                thread.start()
                
                inv.save()
                messages.info(request,f" Bravo, vous avez invité  { nom} à administrer { famille.nom }  !")

            else:
                messages.danger(request,f" Desolé, vous n'avez pas le droit d'administrer { famille.nom }  !")
        else:
            messages.danger(request,f" Desolé, vous n'avez pas le droit d'administrer { famille.nom }  !")
            
    return redirect("edit_famille",id=famille.id )

def mes_messages(request):
    try:
        membre = get_membre_from_session(request)
        if not membre:
            return redirect(f"{reverse('login')}?next={request.get_full_path()}")
        # ou selon votre structure : membre = request.user.membre
    except Membre.DoesNotExist:
        return redirect(f"{reverse('login')}?next={request.get_full_path()}") 

    messages = membre.membres_message.all().order_by('-date_ajout')

    communaute_ids = membre.communautes.values_list('id', flat=True)
    famille_ids = membre.familles.values_list('id', flat=True)
    association_ids = membre.associations.values_list('id', flat=True)

    messages = Message.objects.filter(communaute_id__in=communaute_ids)

    mess = Message.objects.filter(
        Q(contactcommunaute=True, communaute_id__in=communaute_ids) |
        Q(contactfamille=True, famille_id__in=famille_ids) |
        Q(contactassociation=True, association_id__in=association_ids)
    ).select_related('expediteur', 'destinataire').order_by('-date_ajout')

    # mes = Message.objects.filter(
    #     contactcommunaute = True,
    #     communaute__in=membre.communautes.all()
    # ).select_related('expediteur', 'destinataire').order_by('-date_ajout')

    # Marquer comme lus les messages reçus
    messages.update(lu=True)

    context = {
        'messages': messages|mess,
        'membre': membre,
    }
    return render(request, 'messages/mes_messages.html', context)

@csrf_exempt
def valide_salleatt(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax :
        if request.method == "POST" :
            data = json.loads(request.body.decode('utf-8'))
            userid = request.session.get("userid","") 
            
            if data.get('salle') is None:
                return JsonResponse({'status': False ,"message": "Famille incorrecte"})
            else: 
                if userid is None:
                    return JsonResponse({'status': False ,"message": "Merci de vous connecter avant tout abonnement !"})
                else:
                    if data.get('direction') is None:
                        return JsonResponse({'status': False ,"message": "Problème de procédure !"})
                    else:
                        user = Membre.objects.get(id=userid)

                        if( data.get("direction") == "FAM"):
                            # je veux valider l'appartenance d'un membre à une famille
                            salle = SalleAttenteFamille.objects.get(id=data.get("salle"))
                            salle.famille.membres_famille.add(salle.personne)
                            mes = Message(
                                sujet=f" Votre validation d'accès à {salle.famille.nom} ",
                                contenu=f" Un administrateur à validé votre accès à la FAMILLE : {salle.famille.nom}, vous pouvez desormais y acceder .",
                                date_ajout=date.today()
                            )
                            mes.save()
                            salle.personne.messages.add( mes )
                            salle.personne.save()
                            salle.famille.save()
                            message = f"Merci {salle.personne.nomcomplet} , a été autorisé a adherer à  {salle.famille.nom} "
                        else:
                            if( data.get("direction") == "COM"):
                                salle = SalleAttenteCommunaute.objects.get(id=data.get("salle"))
                                salle.communaute.membres_communaute.add(salle.personne)
                                mes = Message(
                                    sujet=f" Votre validation d'accès à {salle.communaute.nom} ",
                                    contenu=f" Un administrateur à validé votre accès à la COMMUNAUTE : {salle.communaute.nom}, vous pouvez desormais y acceder .",
                                    date_ajout=date.today()
                                )
                                 
                                mes.save()
                                salle.personne.messages.add( mes )
                                salle.personne.save()
                                salle.communaute.save()
                                message = f"Merci {salle.personne.nomcomplet} , a été autorisé a adherer à  {salle.communaute.nom} "
                            else:
                                if( data.get("direction") == "ASSO"):
                                    salle = SalleAttenteAssociation.objects.get(id=data.get("salle"))
                                    salle.association.membres_association.add(salle.personne)
                                    mes = Message(
                                        sujet=f" Votre validation d'accès à {salle.association.nom} ",
                                        contenu = f" Un administrateur à validé votre accès à l'ASSOCIATION : {salle.association.nom}, vous pouvez desormais y acceder .",
                                        date_ajout = date.today()
                                    )
                                    
                                    mes.save()
                                    salle.personne.messages.add( mes )
                                    salle.personne.save()
                                    salle.association.save()
                                    message = f"Merci {salle.personne.nomcomplet} , a été autorisé a adherer à  {salle.association.nom} "
                                else:
                                    # je veux valider la fusion  de deux familles 
                                    if( data.get("direction") == "FAMMERE"):

                                        salle = SalleAttenteFamilleMere.objects.get(id=data.get("salle"))

                                        salle.statut = 'accepte'
                                        salle.famille.famille_mere =  salle.famillemere
                                        salle.famillemere.familles_enfant.add(salle.famille)
                                        salle.famille.save()
                                        salle.famillemere.save()
                                        # salle.approuver(user)

                                        mes = Message(
                                            sujet=f" Votre validation de la fusion  de  {salle.famille.nom}  à {salle.famillemere.nom} ",
                                            contenu = f" Un administrateur à validé votre fusion de { salle.famille.nom} à {salle.famillemere.nom} , vous pouvez desormais y acceder .",
                                            date_ajout = date.today()
                                        )
                                        
                                        mes.save()
                                        salle.personne.messages.add( mes )
                                        salle.personne.save()
                                        # salle.save()
                                        message = f" Un administrateur à validé votre fusion de { salle.famille.nom} à {salle.famillemere.nom} , vous pouvez desormais y acceder ."
                                    else: 
                                        return JsonResponse({'status': False ,"message": "Probleme de procedure de fusion des familles !"})
                        
                        salle.validateur =  user
                        salle.date_validation =  date.today()
                        salle.valide = True
                        
                        salle.save()
                        #  ici je peux aussi envoyer un mail à l'utilisateur
                        return JsonResponse({'status': True ,"message": message})
               

@csrf_exempt
def add_user_salleattfam(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax :
        if request.method == "POST" :
            data = json.loads(request.body.decode('utf-8'))
            userid = request.session.get("userid","")
            # user = f' un: {request.session.get("username","")} ,id: {request.session.get("userid","")},n: {request.session.get("nomocomplet","")}'
            # print(data ,data.get("code"))
            
            if data.get('famid') is None:
                return JsonResponse({'status': False ,"message": "Famille incorrecte"})
            else: 
                if userid is None:
                    return JsonResponse({'status': False ,"message": "Merci de vous connecter avant tout abonnement !"})
                else:
                    user = Membre.objects.get(id=userid)
                    famille = Famille.objects.get(id=data.get("famid"))
                
                    ab = SalleAttenteFamille.objects.filter(personne=user, famille=famille)
                    # print(ab, plan, user)
                    if len(ab) == 0: 
                        ab = SalleAttenteFamille( 
                            personne = user,
                            famille= famille, 
                        )
                        ab.save() 
                        message = f"Merci {user.nomcomplet} , votre sollitation d'adherer à la famille {famille.nom} a été prise en compte, un administrateur vous reviendrait dès la fin de l'etude"
                        
                        return JsonResponse({'status': True ,"message": message})
                    else:
                        return JsonResponse({'status': False ,"message": "Desolé, vous avez etes deja dans la salle d'attente !"})

@csrf_exempt
def add_user_salleattcom(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax :
        if request.method == "POST" :
            data = json.loads(request.body.decode('utf-8'))
            userid = request.session.get("userid","") 
            
            if data.get('comid') is None:
                return JsonResponse({'status': False ,"message": "Communauté incorrecte"})
            else: 
                if userid is None:
                    return JsonResponse({'status': False ,"message": "Merci de vous connecter avant tout abonnement !"})
                else:
                    user = Membre.objects.get(id=userid)
                    com = Communaute.objects.get(id=data.get("comid"))
                
                    ab = SalleAttenteCommunaute.objects.filter(personne=user, communaute=com)
                    # print(ab, plan, user)
                    if len(ab) == 0: 
                        ab = SalleAttenteCommunaute( 
                            personne = user,
                            communaute = com, 
                        )
                        ab.save() 
                        message = f"Merci {user.nomcomplet} , votre sollitation d'adherer à la communauté {com.nom} a été prise en compte, un administrateur vous reviendrait dès la fin de l'etude"
                        
                        return JsonResponse({'status': True ,"message": message})
                    else:
                        return JsonResponse({'status': False ,"message": "Desolé, vous avez etes deja dans la salle d'attente !"})

def faq(request):
    return render(request, "archcore/faq.html", {} )

def faqindex(request):
    return render(request, "includes/faqindex.html", {} )


@csrf_exempt
def add_user_salleattasso(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax :
        if request.method == "POST" :
            data = json.loads(request.body.decode('utf-8'))
            userid = request.session.get("userid","") 
            
            if data.get('assoid') is None:
                return JsonResponse({'status': False ,"message": "Association incorrecte"})
            else: 
                if userid is None:
                    return JsonResponse({'status': False ,"message": "Merci de vous connecter avant tout abonnement !"})
                else:
                    user = Membre.objects.get(id=userid)
                    asso = Association.objects.get(id=data.get("assoid"))
                
                    ab = SalleAttenteAssociation.objects.filter(personne=user, association=asso)
                    # print(ab, plan, user)
                    if len(ab) == 0: 
                        ab = SalleAttenteAssociation( 
                            personne = user,
                            association = asso, 
                        )
                        ab.save() 
                        message = f"Merci {user.nomcomplet} , votre sollitation d'adherer à l'association {asso.nom} a été prise en compte, un administrateur vous reviendrait dès la fin de l'etude"
                        
                        return JsonResponse({'status': True ,"message": message})
                    else:
                        return JsonResponse({'status': False ,"message": "Desolé, vous avez etes deja dans la salle d'attente !"})


# Afficher les messages d'une librairie
@require_http_methods(["GET"])
def library_messages(request, library_id):

    lib = Librairie.objects.get(id=library_id)
    messages = LibrairieMessage.objects.filter(librairie=library_id)
    
    context = {
        'library_id': library_id,
        'library_name': f'{lib.nom}',
        'description': f'{lib.description}',
        'lesmessages': messages,
        'total_messages': len(messages)
    }
    return render(request, 'libcore/lib_messages.html', context)


# Créer un message dans une librairie
@require_http_methods(["POST"])
def create_library_message(request):

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax :
        if request.method == "POST" :
            data = json.loads(request.body.decode('utf-8'))
            userid = request.session.get("userid","") 
            
            if data.get('id') is None:
                return JsonResponse({'status': False ,"message": "Librairie incorrecte"})
            else: 
                if userid is None or userid =="":
                    return JsonResponse({'status': False ,"message": "Merci de vous connecter avant de laisser le message !"})
                else:
                    user = Membre.objects.get(id=userid)
                    lib = Librairie.objects.get(id=data.get("id"))

                    username = data.get('nom')
                    message = data.get('message')

                    if not username or not message:
                        return JsonResponse({'error': 'Tous les champs sont requis'}, status=400)

                    if len(message) > 5000:
                        return JsonResponse({'error': 'Le message est trop long (max 5000 caractères)'}, status=400)
                    
                    mes = LibrairieMessage.objects.filter(librairie=lib,user=user,username=username,message=message)
                    if mes != None and mes.count() >0 :
                        return JsonResponse({'error': 'Désolé, Vous avez déjà envoyé ce message'}, status=400)

                    message = LibrairieMessage(
                        librairie=lib,
                        user=user,
                        username=username,
                        message=message
                    )
                    message.save() 

                    return JsonResponse({
                        'success': True,
                        'message': 'Message créé avec succès',
                        # 'data': JsonResponse(message)
                    })

