
from django.shortcuts import redirect, render
from arch_portal.domain.forms.famille import FamilleForm
from arch_portal.domain.models.communaute import Communaute
from arch_portal.domain.models.famille import Famille

def listfamilles(request, id):
   
    livres = Famille.objects.filter(communaute=id)
    lib = Communaute.objects.get(id=id) 
    return render(request, "archcore/listfamilles.html", { "familles" : livres, "communaute" : lib } )

def show_famille(request,id):
    liv = Famille.objects.get(id=id)
    # print( "membres: {}".format(liv.get_members()) )
    return render(request, "archcore/showfamille.html", {"famille" : liv} )

def add_famille(request):
    
    if request.method == "POST":
        form = FamilleForm(request.POST)
        if form.is_valid():  
            com = form.save() 
            com.save()
            return redirect("show_famille",com.id )
    else:
        form = FamilleForm()

    return render(request, "archcore/new_famille.html", { "form":form  })
