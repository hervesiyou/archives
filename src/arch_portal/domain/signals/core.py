from django.db.models.signals import post_save
from django.dispatch import receiver
from arch_portal.domain.models.membre import Membre
from arch_portal.domain.models.wallet import Wallet

@receiver(post_save, sender=Membre)
def create_default_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(
            membre=instance,          # ou membre=instance selon ton modèle Wallet
            solde=0.00,
            devise='XAF',           # ou 'EUR', 'USD' — adapte selon ton besoin
        )