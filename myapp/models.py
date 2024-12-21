from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Avion(models.Model):
    type_avion = models.CharField(max_length=4, editable=False)
    date_mise_service = models.DateField(auto_now_add=True, editable=False)
    heures_vol_der_rev = models.PositiveIntegerField(default=0)
    heures_vol = models.PositiveIntegerField(default=0)
    date_der_rev = models.DateTimeField(null=True)

class Rapport(models.Model):
    avion = models.ForeignKey(Avion, on_delete=models.CASCADE, related_name="rapports")
    texte = models.TextField()
    heures_vol = models.PositiveIntegerField(default=0)
    date = models.DateField(auto_now_add=True, editable=False)


class Employe(models.Model):
    is_navigant = models.BooleanField()
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    date_embauche = models.DateField(auto_now_add=True, editable=False)
    # should add: fonction, phone_number, salaire

class EmployeNavigant(models.Model):
    avions = models.ManyToManyField(Avion, related_name="equipe")
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name="navigant")
    heures_vol = models.PositiveIntegerField(default=0)
    heures_mois_vol = models.PositiveIntegerField(default=0)


class Ville(models.Model):
    nom = models.CharField(max_length=50)
    nom_pays = models.CharField(max_length=50)


class Jour(models.Model):
    LUNDI = "LU"
    MARDI = "MA"
    MERCREDI = "ME"
    JEUDI = "JE"
    VENDREDI = "VE"
    SAMEDI = "SA"
    DIMANCHE = "DI"
    JOUR_CHOICES = {
        LUNDI: "lundi",
        MARDI: "mardi",
        MERCREDI: "mercredi",
        JEUDI: "jeudi",
        VENDREDI: "vendredi",
        SAMEDI: "samedi",
        DIMANCHE: "dimanche"
    }

    jour = models.CharField(max_length=2, choices=JOUR_CHOICES)


class Vol(models.Model):
    avion = models.ForeignKey(Avion, on_delete=models.SET_NULL, related_name="vols", null=True)
    depart = models.ForeignKey(Ville, on_delete=models.CASCADE, related_name="depart_vols")
    arrive = models.ForeignKey(Ville, on_delete=models.CASCADE, related_name="arrive_vols")
    heure_depart = models.TimeField()
    duree = models.DurationField() #en millisecondes
    jours = models.ManyToManyField(Jour, related_name="vols")


class Escale(models.Model):
    vol = models.ForeignKey(Vol, on_delete=models.CASCADE, related_name="escales")
    ville = models.ForeignKey(Ville, on_delete=models.CASCADE, related_name="escales")
    heure_arrive = models.TimeField()
    duree = models.DurationField() #en millisecondes
    no_ord = models.PositiveIntegerField(default=0)