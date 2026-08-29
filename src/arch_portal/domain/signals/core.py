from django.db.models.signals import post_save
from django.dispatch import receiver
from arch_portal.domain.models.membre import Membre
from arch_portal.domain.models.plantarifaire import Plan
from arch_portal.domain.models.abonnement import Abonnement
from arch_portal.domain.models.wallet import Wallet
from arch_portal.use_cases.services.core import generate_code_membre_abo

@receiver(post_save, sender=Membre)
def create_default_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(
            membre=instance,          # ou membre=instance selon ton modèle Wallet
            solde=0.00,
            devise='XAF',           # ou 'EUR', 'USD' — adapte selon ton besoin
        )

# @receiver(post_save, sender=Membre)
# def creer_default_abonnement(sender, instance, created, **kwargs):
#     if created:
#         plan= Plan.plan_default()
#         Abonnement.objects.create(
#             membre=instance,
#             plan=plan,
#             prix=0,
#             code=generate_code_membre_abo(instance.nomcomplet,plan)
#         )