from django.db import models


class Message(models.Model):
    class Meta:
        verbose_name = " Message"
        verbose_name_plural = "Les Messages"
    
    sujet = models.CharField(max_length=100)
    contenu = models.CharField(max_length=250)
    date_ajout = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.sujet} , {self.date_ajout}"