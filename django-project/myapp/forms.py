from django import forms
from .models import Vol, Escale, Avion, Employe, Rapport, EmployeNavigant, Ville

class VolForm(forms.ModelForm):
    class Meta:
        model = Vol
        fields = ["avion", "depart", "arrive", "heure_depart", "duree", "jours"]

class EscaleForm(forms.ModelForm):
    class Meta:
        model = Escale
        fields = ["ville", "heure_arrive", "duree", "no_ord"]
        
class AvionForm(forms.ModelForm):
    class Meta:
        model = Avion
        fields = ["type_avion"]
        

class EmployeForm(forms.ModelForm):
    class Meta:
        model = Employe
        fields = ["is_navigant", "nom", "prenom", "fonction", "phone_number", "salaire"]

class RapportForm(forms.ModelForm):
    class Meta:
        model = Rapport
        fields = ['avion', 'texte', 'heures_vol']

class EmployeNavigantForm(forms.ModelForm):
    class Meta:
        model = EmployeNavigant
        fields = ['employe', 'avions', 'heures_vol', 'heures_mois_vol']

class VilleForm(forms.ModelForm):
    class Meta:
        model = Ville
        fields = ['nom', 'nom_pays']