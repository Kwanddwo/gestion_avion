from django import forms
from .models import Vol, Avion

class VolForm(forms.ModelForm):
    class Meta:
        model = Vol
        fields = ["avion", "depart", "arrive", "heure_depart", "duree", "jours"]

class AvionForm(forms.Form):
    pass