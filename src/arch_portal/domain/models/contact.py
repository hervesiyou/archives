
from django.db import models 

from datetime import datetime
class Contact(models.Model):    

    email = models.EmailField(verbose_name="Addresse Email")
    sender = models.CharField(max_length=200, verbose_name="Utilisateur")
    # subject = models.CharField(max_length=200, verbose_name="Sujet")
    message = models.TextField(verbose_name="Message")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    def __str__(self):
        return f"Contact de {self.email} à propose de {self.sender} "
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.created_at = datetime.now()

    class Meta:
        verbose_name = "Contact des Utilisateurs"
        verbose_name_plural = "Les Contacts - Utilisateurs"
        ordering = ['-created_at']
        db_table = 'arch_portal_contact'
