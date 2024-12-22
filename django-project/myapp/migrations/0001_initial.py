# Generated by Django 5.1.4 on 2024-12-22 13:36

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Avion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_avion', models.CharField(max_length=4)),
                ('date_mise_service', models.DateField(auto_now_add=True)),
                ('heures_vol_der_rev', models.PositiveIntegerField(default=0)),
                ('heures_vol', models.PositiveIntegerField(default=0)),
                ('date_der_rev', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_navigant', models.BooleanField()),
                ('nom', models.CharField(max_length=50)),
                ('prenom', models.CharField(max_length=50)),
                ('date_embauche', models.DateField(auto_now_add=True)),
                ('fonction', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=15)),
                ('salaire', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Jour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jour', models.CharField(choices=[('LU', 'lundi'), ('MA', 'mardi'), ('ME', 'mercredi'), ('JE', 'jeudi'), ('VE', 'vendredi'), ('SA', 'samedi'), ('DI', 'dimanche')], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Ville',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50)),
                ('nom_pays', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Rapport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texte', models.TextField()),
                ('heures_vol', models.PositiveIntegerField(default=0)),
                ('date', models.DateField(auto_now_add=True)),
                ('avion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rapports', to='myapp.avion')),
            ],
        ),
        migrations.CreateModel(
            name='Vol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heure_depart', models.TimeField()),
                ('duree', models.DurationField()),
                ('arrive', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arrive_vols', to='myapp.ville')),
                ('avion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vols', to='myapp.avion')),
                ('depart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='depart_vols', to='myapp.ville')),
                ('jours', models.ManyToManyField(related_name='vols', to='myapp.jour')),
            ],
        ),
        migrations.CreateModel(
            name='Escale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heure_arrive', models.TimeField()),
                ('duree', models.DurationField()),
                ('no_ord', models.PositiveIntegerField(default=0)),
                ('ville', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='escales', to='myapp.ville')),
                ('vol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='escales', to='myapp.vol')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeNavigant',
            fields=[
                ('employe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='navigant', serialize=False, to='myapp.employe')),
                ('heures_vol', models.PositiveIntegerField(default=0)),
                ('heures_mois_vol', models.PositiveIntegerField(default=0)),
                ('avions', models.ManyToManyField(related_name='equipe', to='myapp.avion')),
            ],
        ),
    ]
