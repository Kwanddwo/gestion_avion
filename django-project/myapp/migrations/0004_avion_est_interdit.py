# Generated by Django 5.1.4 on 2024-12-24 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_alter_employe_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='avion',
            name='est_interdit',
            field=models.BooleanField(default=False),
        ),
    ]
