from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from datetime import date, timedelta

class User(AbstractUser):
    pass

MAX_DAYS = 30 * 6
MAX_HEURES_VOL = 1000
class Avion(models.Model):
    type_avion = models.CharField(max_length=4)
    date_mise_service = models.DateField(auto_now_add=True, help_text="Format: YYYY-MM-DD")
    heures_vol_der_rev = models.PositiveIntegerField(default=0)
    heures_vol = models.PositiveIntegerField(default=0)
    date_der_rev = models.DateField(null=True)
    est_interdit = models.BooleanField(default=False)
    def rapport(self):
        self.heures_vol_der_rev = 0
        self.date_der_rev = date.today()
        self.est_interdit = False
    def interdit(self):
        if self.heures_vol_der_rev > MAX_HEURES_VOL or self.date_der_rev < date.today() - timedelta(days=MAX_DAYS):
            self.est_interdit = True
    def add_heures_vol(self, vol):
        if not isinstance(vol, Vol):
            raise TypeError("argument vol is not of type Vol")
        heures_vol = int(vol.duree.total_seconds() / timedelta(hours=1).total_seconds())
        self.heures_vol += heures_vol
        self.heures_vol_der_rev += heures_vol
        self.interdit()
    def __str__(self):
        return f"N° {self.pk} - type {self.type_avion}"

class Rapport(models.Model):
    avion = models.ForeignKey(Avion, on_delete=models.CASCADE, related_name="rapports")
    texte = models.TextField()
    heures_vol = models.PositiveIntegerField(default=0)
    date = models.DateField(default=date.today(), help_text="Format: YYYY-MM-DD")
    def __str__(self):
        return f"Rapport pour avion {self.avion} - {self.date}"

# phone_number validator
class Employe(models.Model):
    is_navigant = models.BooleanField()
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    date_embauche = models.DateField(auto_now_add=True, editable=False, help_text="Format: YYYY-MM-DD")
    fonction = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, validators=[RegexValidator(r"^[\d\s+\-]+$")])
    salaire = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.fonction} {"navigant" if self.is_navigant else "non-navigant"}"
    

class EmployeNavigant(models.Model):
    avions = models.ManyToManyField(Avion, related_name="equipe", blank=True)
    employe = models.OneToOneField(Employe, on_delete=models.CASCADE, related_name="navigant", primary_key=True)
    heures_vol = models.PositiveIntegerField(default=0)
    heures_mois_vol = models.PositiveIntegerField(default=0)
    def add_heures_vol(self, vol):
        if not isinstance(vol, Vol):
            raise TypeError("argument vol is not of type Vol")
        heures_vol = int(vol.duree.total_seconds() / timedelta(hours=1).total_seconds())
        self.heures_vol += heures_vol
        self.heures_mois_vol += heures_vol
    def __str__(self):
        return f"Navigant {self.employe} - {self.heures_vol} heures de vol"


class Ville(models.Model):
    nom = models.CharField(max_length=50)
    nom_pays = models.CharField(max_length=50)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['nom', 'nom_pays'], name='unique_city_country')
        ]
    def __str__(self):
        return f"{self.nom}, {self.nom_pays}"


class Jour(models.Model):
    LUNDI = "LU"
    MARDI = "MA"
    MERCREDI = "ME"
    JEUDI = "JE"
    VENDREDI = "VE"
    SAMEDI = "SA"
    DIMANCHE = "DI"
    JOUR_CHOICES = {
        LUNDI: "Lundi",
        MARDI: "Mardi",
        MERCREDI: "Mercredi",
        JEUDI: "Jeudi",
        VENDREDI: "Vendredi",
        SAMEDI: "Samedi",
        DIMANCHE: "Dimanche"
    }

    jour = models.CharField(max_length=2, choices=JOUR_CHOICES)
    def __str__(self):
        return self.JOUR_CHOICES[self.jour]

class Vol(models.Model):
    avion = models.ForeignKey(Avion, on_delete=models.SET_NULL, related_name="vols", null=True)
    depart = models.ForeignKey(Ville, on_delete=models.CASCADE, related_name="depart_vols")
    arrive = models.ForeignKey(Ville, on_delete=models.CASCADE, related_name="arrive_vols")
    heure_depart = models.TimeField(help_text="Format: HH:MM:SS")
    duree = models.DurationField(help_text="Format: D HH:MM:SS") #en deltatime
    jours = models.ManyToManyField(Jour, related_name="vols")
    def __str__(self):
        return f"Vol de {self.depart} à {self.arrive} ({self.heure_depart})"

class Escale(models.Model):
    vol = models.ForeignKey(Vol, on_delete=models.CASCADE, related_name="escales")
    ville = models.ForeignKey(Ville, on_delete=models.CASCADE, related_name="escales")
    heure_arrive = models.TimeField(help_text="Format: HH:MM:SS")
    duree = models.DurationField(help_text="Format: D HH:MM:SS") #en millisecondes
    no_ord = models.PositiveIntegerField(default=0)
    def __str__(self):
        return f"Escale (n° {self.no_ord}) à {self.ville} pour le vol {self.vol} (Arrivée: {self.heure_arrive})"