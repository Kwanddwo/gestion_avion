from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class User(AbstractUser):
    pass

class Avion(models.Model):
    type_avion = models.CharField(max_length=4)
    date_mise_service = models.DateField(auto_now_add=True)
    heures_vol_der_rev = models.PositiveIntegerField(default=0)
    heures_vol = models.PositiveIntegerField(default=0)
    date_der_rev = models.DateField(null=True)
    def __str__(self):
        return f"Avion {self.type_avion} (ID: {self.pk} Mise en service: {self.date_mise_service})"

class Rapport(models.Model):
    avion = models.ForeignKey(Avion, on_delete=models.CASCADE, related_name="rapports")
    texte = models.TextField()
    heures_vol = models.PositiveIntegerField(default=0)
    date = models.DateField(auto_now_add=True, editable=False)
    def __str__(self):
        return f"Rapport pour {self.avion} - {self.date}"

# phone_number validator
class Employe(models.Model):
    is_navigant = models.BooleanField()
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    date_embauche = models.DateField(auto_now_add=True, editable=False)
    fonction = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, validators=[RegexValidator("^[\d\s+\-]+$")])
    salaire = models.DecimalField(max_digits=10, decimal_places=2)
    #def __str__(self):
        #return f"{self.prenom} {self.nom} - {self.fonction} {"navigant" if self.is_navigant else "non-navigant"}"
    

class EmployeNavigant(models.Model):
    avions = models.ManyToManyField(Avion, related_name="equipe", blank=True)
    employe = models.OneToOneField(Employe, on_delete=models.CASCADE, related_name="navigant", primary_key=True)
    heures_vol = models.PositiveIntegerField(default=0)
    heures_mois_vol = models.PositiveIntegerField(default=0)
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
        LUNDI: "lundi",
        MARDI: "mardi",
        MERCREDI: "mercredi",
        JEUDI: "jeudi",
        VENDREDI: "vendredi",
        SAMEDI: "samedi",
        DIMANCHE: "dimanche"
    }

    jour = models.CharField(max_length=2, choices=JOUR_CHOICES)
    def __str__(self):
        return self.JOUR_CHOICES[self.jour]

class Vol(models.Model):
    avion = models.ForeignKey(Avion, on_delete=models.SET_NULL, related_name="vols", null=True)
    depart = models.ForeignKey(Ville, on_delete=models.CASCADE, related_name="depart_vols")
    arrive = models.ForeignKey(Ville, on_delete=models.CASCADE, related_name="arrive_vols")
    heure_depart = models.TimeField()
    duree = models.DurationField() #en millisecondes
    jours = models.ManyToManyField(Jour, related_name="vols")
    def __str__(self):
        return f"Vol de {self.depart} à {self.arrive} ({self.heure_depart})"

class Escale(models.Model):
    vol = models.ForeignKey(Vol, on_delete=models.CASCADE, related_name="escales")
    ville = models.ForeignKey(Ville, on_delete=models.CASCADE, related_name="escales")
    heure_arrive = models.TimeField()
    duree = models.DurationField() #en millisecondes
    no_ord = models.PositiveIntegerField(default=0)
    def __str__(self):
        return f"Escale (n° {self.no_ord}) à {self.ville} pour le vol {self.vol} (Arrivée: {self.heure_arrive})"