# Generated by Django 5.0.7 on 2024-08-21 14:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arch_portal', '0003_commandelivre'),
    ]

    operations = [
        migrations.AddField(
            model_name='famille',
            name='famille_mere',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='arch_portal.famille'),
        ),
    ]