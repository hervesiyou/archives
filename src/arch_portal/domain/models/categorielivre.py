# categorie.py
from django.db import models
from django.utils.crypto import get_random_string

class Categorie(models.Model):
    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories de livres"
        ordering = ["titre"]

    titre = models.CharField(max_length=150)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="categories/", null=True, blank=True)

    def __str__(self):
        return self.titre
    
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_code(10) 

        super().save(*args, **kwargs)
    
    @staticmethod
    def generate_code(length=10):
        return "CAT-" + get_random_string(
            length,
            allowed_chars='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        )
