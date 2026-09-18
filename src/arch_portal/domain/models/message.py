from django.db import models


class Message(models.Model):
    class Meta:
        verbose_name = " Message"
        verbose_name_plural = "Les Messages"
    
    sujet = models.CharField(max_length=100)
    contenu = models.CharField(max_length=250)

    contactfamille = models.BooleanField(default=False, help_text="Cochez cette case si le message est destiné à la famille", null=True, blank=True)
    contactcommunaute = models.BooleanField(default=False, help_text="Cochez cette case si le message est destiné à la communauté", null=True, blank=True)
    contactassociation = models.BooleanField(default=False, help_text="Cochez cette case si le message est destiné à l'association", null=True, blank=True)

    communaute = models.ForeignKey('Communaute', on_delete=models.CASCADE, related_name='communaute_messages', null=True, blank=True)
    association = models.ForeignKey('Association', on_delete=models.CASCADE, related_name='association_messages', null=True, blank=True)
    famille = models.ForeignKey('Famille', on_delete=models.CASCADE, related_name='famille_messages', null=True, blank=True)

    destinataire = models.ForeignKey('Membre', on_delete=models.CASCADE, related_name='membres_message', null=True, blank=True)
    expediteur = models.ForeignKey('Membre', on_delete=models.CASCADE, related_name='membres_expediteur', null=True, blank=True)
    lu = models.BooleanField(default=False)

    actif = models.BooleanField(default=False)

    date_ajout = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.sujet} , {self.date_ajout}"