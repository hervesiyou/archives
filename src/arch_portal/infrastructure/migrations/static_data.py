from django.db import migrations

def add_static_data(apps, schema_editor):

        marches = apps.get_model('arch_portal', 'Marche')
        membres = apps.get_model('arch_portal', 'Membre')
        communaute = apps.get_model('arch_portal', 'Communaute')
        famille = apps.get_model('arch_portal', 'Famille')
        librairie = apps.get_model('arch_portal', 'Librairie') 

        # Insert country
        ipocrate, _ = marches.objects.get_or_create(nom="Ipocrate", description="Des packages de prise en charge, des produits bio et les services de laboratoire pour vous",lien="https://ipocrate.org")

        konda, _ = marches.objects.get_or_create(nom="KondaShop", description="Le commerce autrement",lien="https://kondashop.com")

class Migration(migrations.Migration):

    dependencies = [
        ('arch_portal', '0001_initial'),
    ]

    
    operations = [
        migrations.RunPython(add_static_data),
    ]