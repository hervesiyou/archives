from django.db import models 

class CommandeLivre(models.Model):
    class Meta:
        verbose_name = "Commande de Livre"
        verbose_name_plural = "Les commandes "
    
    db_table = "commandes_livres"
    nom = models.CharField(max_length=150)
    telephone = models.CharField(max_length=150)
    date= models.DateTimeField(auto_now=True, auto_now_add=False) 
    message = models.TextField( blank=True)
    proprietaire = models.ForeignKey(
        "Membre",
        on_delete=models.SET_NULL,
        blank=True,null=1
    )
    librairie = models.ForeignKey(
        "Librairie",
        on_delete=models.SET_NULL,
        blank=True,null=1
    )
    livre = models.ForeignKey(
        "Livre",
        on_delete=models.SET_NULL,
        blank=True,null=1
    )
    def __str__(self):
        return f"{self.nom} = {self.livre.nom}"
    