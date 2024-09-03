# Generated by Django 5.0.7 on 2024-09-03 07:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arch_portal', '0005_merge_0004_famille_famille_mere_static_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='association',
            name='adhesion',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='association',
            name='contact',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='association',
            name='localisation',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='famille',
            name='chef',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mon_chef', to='arch_portal.membre'),
        ),
        migrations.AlterField(
            model_name='famille',
            name='communaute',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='arch_portal.communaute'),
        ),
        migrations.AlterField(
            model_name='famille',
            name='famille_mere',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='arch_portal.famille'),
        ),
        migrations.CreateModel(
            name='Evenement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('titre', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('periodicite', models.CharField(max_length=50)),
                ('communaute', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='arch_portal.communaute')),
            ],
            options={
                'verbose_name': 'Evenements',
                'verbose_name_plural': ' Les Evenements ',
            },
        ),
    ]