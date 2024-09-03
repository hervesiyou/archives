# Generated by Django 5.0.7 on 2024-07-30 18:44

import django.db.models.deletion
from django.db import migrations, models



class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Association',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=150)),
                ('description', models.TextField(blank=True)),
                ('type', models.CharField(blank=True, choices=[('Danse', 'Danse du Village'), ('Reunion', 'Reunion associative')], max_length=50, null=1)),
            ],
            options={
                'verbose_name': 'Association',
                'verbose_name_plural': 'Les Associations',
            },
        ),
        migrations.CreateModel(
            name='Communaute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=150)),
                ('description', models.TextField(default='')),
                ('superficie', models.CharField(default=0, max_length=50)),
                ('histoire', models.TextField(blank=True, default='')),
                ('geographie', models.TextField(blank=True, default='')),
                ('origine', models.CharField(default='', max_length=150)),
                ('type', models.CharField(blank=True, choices=[('Village', 'Village'), ('Diapora', 'Communauté Diaspora'), ('Groupe', 'Groupement')], max_length=50, null=1)),
                ('region', models.CharField(blank=True, choices=[('North', 'North'), ('South', 'South'), ('East', 'East'), ('West', 'West'), ('Center', 'Center'), ('Littoral', 'Littoral'), ('South-West', 'South West'), ('North-West', 'North West'), ('Adamaoua', 'Adamaoua'), ('Extrem-North', 'Extrem North')], max_length=50, null=1)),
            ],
            options={
                'verbose_name': 'Communauté',
                'verbose_name_plural': ' Les Communautés ',
            },
        ),
        migrations.CreateModel(
            name='Galerie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=250)),
                ('description', models.TextField(null=True)),
            ],
            options={
                'verbose_name': 'Galerie',
                'verbose_name_plural': 'Les Galeries',
            },
        ),
        migrations.CreateModel(
            name='Librairie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('type', models.CharField(blank=True, choices=[('Physique', 'Librairie Physique'), ('Digitale', 'Librairie Digitale')], max_length=50)),
                ('lieu', models.CharField(max_length=250, null=True)),
            ],
            options={
                'verbose_name': 'Librairie ',
                'verbose_name_plural': '  Les Librairies ',
            },
        ),
        migrations.CreateModel(
            name='Famille',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('histoire', models.TextField(blank=True, null=True)),
                ('origine', models.TextField(blank=True, null=True)),
                ('type', models.CharField(blank=True, max_length=50)),
                ('communaute', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='arch_portal.communaute')),
                ('galeries', models.ManyToManyField(blank=True, null=True, related_name='galeries_famille', to='arch_portal.galerie')),
            ],
            options={
                'verbose_name': 'Famille',
                'verbose_name_plural': 'Les Familles',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50)),
                ('galerie', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ma_galerie', to='arch_portal.galerie')),
            ],
        ),
        migrations.AddField(
            model_name='galerie',
            name='images',
            field=models.ManyToManyField(blank=True, related_name='mes_images', to='arch_portal.image'),
        ),
        migrations.CreateModel(
            name='Livre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=150)),
                ('description', models.TextField(null=True)),
                ('auteur', models.CharField(max_length=250)),
                ('domaine', models.CharField(blank=True, max_length=250, null=True)),
                ('prix', models.IntegerField(default=0)),
                ('librairies', models.ManyToManyField(null=True, related_name='mes_librairies', to='arch_portal.librairie')),
            ],
            options={
                'verbose_name': '  Livre de bibliotheque ',
                'verbose_name_plural': ' Les  Livres',
            },
        ),
        migrations.AddField(
            model_name='librairie',
            name='livres',
            field=models.ManyToManyField(blank=True, null=True, related_name='mes_livres', to='arch_portal.livre'),
        ),
        migrations.CreateModel(
            name='Membre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomcomplet', models.CharField(max_length=100)),
                ('login', models.CharField(max_length=50)),
                ('pwd', models.CharField(max_length=50)),
                ('etatvalidation', models.BooleanField(default=0, null=True)),
                ('dateinscription', models.DateTimeField(null=True)),
                ('type', models.CharField(blank=True, choices=[('Chef', 'CHEF'), ('Admin', 'ADMINISTRATEUR'), ('Membre', 'MEMBRE')], max_length=50, null=1)),
                ('sexe', models.CharField(blank=True, choices=[('F', 'Female'), ('M', 'Male')], max_length=50, null=1)),
                ('datenaissance', models.CharField(max_length=50, null=True)),
                ('lieunaissance', models.CharField(blank=True, max_length=50, null=True)),
                ('residence', models.CharField(blank=True, max_length=150, null=True)),
                ('etatcivil', models.CharField(choices=[('Celibataire', 'Celibataire'), ('Marie', 'Marié Monogame'), ('Polygame', 'Marié Polygame')], max_length=50, null=True)),
                ('nbenfant', models.IntegerField(default=0)),
                ('notabilite', models.CharField(blank=True, max_length=250, null=True)),
                ('education', models.CharField(blank=True, max_length=250, null=True)),
                ('diplomes', models.CharField(blank=True, max_length=250, null=True)),
                ('profession', models.CharField(blank=True, max_length=150, null=True)),
                ('pere', models.CharField(max_length=150)),
                ('mere', models.CharField(max_length=150)),
                ('vivant', models.BooleanField(default=True)),
                ('datedeces', models.CharField(blank=True, max_length=50, null=True)),
                ('approbateurs', models.ManyToManyField(blank=True, null=True, to='arch_portal.membre')),
                ('associations', models.ManyToManyField(blank=True, null=True, to='arch_portal.association')),
                ('familles', models.ManyToManyField(null=True, related_name='mes_familles', to='arch_portal.famille')),
                ('galeries', models.ManyToManyField(blank=True, null=True, related_name='mes_galeries', to='arch_portal.galerie')),
                ('images', models.ManyToManyField(blank=True, null=True, to='arch_portal.image')),
            ],
            options={
                'verbose_name': ' Membre',
                'verbose_name_plural': 'Les Membres',
            },
        ),
        migrations.CreateModel(
            name='Marche',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('lien', models.CharField(max_length=250, null=True)),
                ('possesseur', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='arch_portal.membre')),
            ],
            options={
                'verbose_name': '  Marché ',
                'verbose_name_plural': '  Nos Marchés  ',
            },
        ),
        migrations.AddField(
            model_name='librairie',
            name='possesseur',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='arch_portal.membre'),
        ),
        migrations.AddField(
            model_name='famille',
            name='chef',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mon_chef', to='arch_portal.membre'),
        ),
        migrations.AddField(
            model_name='communaute',
            name='chef',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='arch_portal.membre'),
        ),

    ]
