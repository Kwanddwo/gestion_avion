# Generated by Django 5.0.4 on 2024-12-19 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_alter_escale_options_alter_escale_no_ord'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='escale',
            constraint=models.UniqueConstraint(fields=('vol', 'no_ord'), name='unique_escale_per_vol'),
        ),
        migrations.AddConstraint(
            model_name='escale',
            constraint=models.UniqueConstraint(fields=('vol', 'ville'), name='unique_ville_per_vol'),
        ),
    ]
