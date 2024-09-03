from django.shortcuts import redirect, render
from arch_portal.domain.forms.evenement import EvenementForm
from arch_portal.domain.models.communaute import Communaute
from arch_portal.domain.models.evenement import Evenement


def listevenements(request, id):
    events = Evenement.objects.filter(communaute=id)
    com = Communaute.objects.get(id=id)
    return render(request, "archcore/listevenements.html", {"evenements": events, "communaute": com})

def show_evenement(request, id):
    event = Evenement.objects.get(id=id)
    return render(request, "archcore/showevenement.html", {"evenement": event})


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
