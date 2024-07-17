from django.shortcuts import render

# Create your views here.
from coreapp.models import *
 

def listmarkets(request):
    mar = Marches.objects.all()
 
    return render(request, "marketcore/listmarches.html", { "marches" : mar, })
