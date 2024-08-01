from django.shortcuts import render 
from arch_portal.domain.models.marche import Marche

def listmarkets(request):
    mar = Marche.objects.all()
    return render(request, "marketcore/listmarches.html", { "marches" : mar, })
