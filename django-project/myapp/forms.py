from django import forms
from .models import Vol, Escale, Avion

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
        fields = ["type"]