from django.shortcuts import redirect, render, get_object_or_404
from arch_portal.domain.forms.evenement import EvenementForm
from arch_portal.domain.models.communaute import Communaute
from arch_portal.domain.models.evenement import Evenement
from arch_portal.domain.models.membre import Membre

# views.py

from django.contrib.auth.decorators import login_required 
from arch_portal.domain.models.evenementlike import EvenementLike
 

def listevenements(request, id, mode=0):
    events = Evenement.objects.filter(communaute=id)
    com = Communaute.objects.get(id=id)
    if not mode: 
        return render(request, "archcore/listevenements_tab.html", {"evenements": events, "communaute": com})
    return render(request, "archcore/listevenements.html", {"evenements": events, "communaute": com})

def show_evenement(request, id):
    # event = Evenement.objects.get(id=id)
    # return render(request, "archcore/showevenement.html", {"evenement": event})

    event = get_object_or_404(Evenement, id=id)
    deja_like = False
    userid = request.session.get("userid","") 
    if userid is not None:
        user = get_object_or_404(Membre, id=id)
        deja_like = EvenementLike.objects.filter( user=user, evenement=event ).exists()

    return render(request, "archcore/showevenement.html", {"evenement": event, "deja_like": deja_like })


@login_required
def mes_evenements_likes(request):
  
    userid = request.session.get("userid","") 
    if userid is not None:
        user = get_object_or_404(Membre, id=userid)
        likes =   EvenementLike.objects.filter(user=user).select_related("evenement", "evenement__communaute").order_by("-created_at")
    else:
        return redirect("login")

    return render(request, "archcore/evenement_likes.html", {"likes": likes })


@login_required
def toggle_like_evenement(request, id):

    event = get_object_or_404(Evenement, id=id)  
    userid = request.session.get("userid","") 
    if userid is not None:
        user = get_object_or_404(Membre, id=userid)  
        like = EvenementLike.objects.filter(  user=user,  evenement=event ).first()
    else:
        return redirect("login")

    if like:
        like.delete()
    else:
        EvenementLike.objects.create( user=user, evenement=event )

    return render(request, "archcore/showevenement.html", {"evenement": event, "deja_like": like })


def add_evenement(request):
    if request.method == "POST":
        form = EvenementForm(request.POST)
        if form.is_valid():
            event = form.save()
            event.save()
            return redirect("show_evenement", event.id)
    else:
        form = EvenementForm()

    return render(request, "archcore/new_evenement.html", {"form": form})
