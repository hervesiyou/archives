from django.db import  models
from  arch_portal.domain  import models as modele

class Evenement(models.Model):
    class Meta:
        verbose_name = "Evenements"
        verbose_name_plural = " Les Evenements "

    db_table = "evenements"
    date=models.DateTimeField(auto_now=True)
    titre=models.CharField(max_length=200)
    description=models.TextField()
    # likes = models.ManytoMany("EvenementLike", related_name="", null=True, blank=True)
    communaute=models.ForeignKey(modele.communaute.Communaute,on_delete=models.SET_NULL,null=True)
    periodicite=models.CharField(max_length=50)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # self.likes.set(0)

    def __str__(self):
        return f"{self.titre} - {self.periodicite}"

    def nombre_likes(self):
        return self.likes.count()