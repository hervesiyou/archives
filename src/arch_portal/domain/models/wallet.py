
from django.db import models
from django.utils.crypto import get_random_string
import random
import string
from .membre import Membre  

class Wallet(models.Model):
    class Meta:
        verbose_name = "Portefeulle"
        verbose_name_plural = "Les portefeulles"

    code = models.CharField(max_length=255, unique=True,     editable=False )
    devise = models.CharField(max_length=255, null=True,     editable=True)
    pub_key = models.CharField( max_length=512, null=True, blank=True    )
    priv_key = models.CharField( max_length=512,  null=True,  blank=True  )
    solde = models.DecimalField(max_digits=12, decimal_places=2,   default=0  )
    membre = models.OneToOneField( Membre,on_delete=models.CASCADE,related_name="wallet", null=True,  blank=True  )
    bankno = models.CharField( max_length=255, null=True,  blank=True  )

    def __str__(self):
        return f"{self.code} {self.solde}"

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_code(10)
        if not self.bankno:
            self.bankno = self.generate_bankno()

        super().save(*args, **kwargs)

    @staticmethod
    def generate_code(length=10):
        return "WAL-" + get_random_string(
            length,
            allowed_chars='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        )
    
    
    def generate_bankno(self):
        initials = ''.join(word[0].upper() for word in self.membre.nomcomplet.split()[:3])
        year = str(self.membre.datenaissance[:4][-2:])[-2:] if self.membre.datenaissance else "25"
        random_suffix = ''.join(random.choices(string.digits, k=6))
        return f"{initials}{year}{random_suffix}XAF"
 