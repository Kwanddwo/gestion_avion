from django import forms
from .models import *
import django_filters

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
        fields = ["type_avion", "heures_vol", "est_interdit"]

class EmployeForm(forms.ModelForm):
    class Meta:
        model = Employe
        fields = ['is_navigant', 'nom', 'prenom', 'fonction', 'phone_number', 'salaire']

class RapportForm(forms.ModelForm):
    class Meta:
        model = Rapport
        fields = ['avion', 'date', 'texte']

class EmployeNavigantForm(forms.ModelForm):
    class Meta:
        model = EmployeNavigant
        fields = ['avions', 'heures_vol', 'heures_mois_vol']

class VilleForm(forms.ModelForm):
    class Meta:
        model = Ville
        fields = ['nom', 'nom_pays']

class AvionFilter(django_filters.FilterSet):
    class Meta:
        model = Avion
        fields = {
            "type_avion": ['icontains'],
            "date_mise_service": ['gte', 'lte'],
            "date_der_rev": ['gte', 'lte'],
            "heures_vol_der_rev": ['gte', 'lte'],
            "heures_vol": ['gte', 'lte']
        }


class RapportFilter(django_filters.FilterSet):
    class Meta:
        model = Rapport
        fields = {
            "avion": ['exact'],
            "heures_vol": ['gte', 'lte'],
            "date": ['gte', 'lte'],
        }



class EmployeFilter(django_filters.FilterSet):
    class Meta:
        model = Employe
        fields = {
            "is_navigant": ['exact'],
            "nom": ['icontains'],
            "prenom": ['icontains'],
            "date_embauche": ['gte', 'lte'],
            "fonction": ['icontains'],
            "phone_number": ['icontains'],
            "salaire": ['gte', 'lte'],
        }


class EmployeNavigantFilter(django_filters.FilterSet):
    class Meta:
        model = EmployeNavigant
        fields = {
            "avions": ['exact'],
            "heures_vol": ['gte', 'lte'],
            "heures_mois_vol": ['gte', 'lte'],
        }


class VilleFilter(django_filters.FilterSet):
    class Meta:
        model = Ville
        fields = {
            "nom": ['icontains'],
            "nom_pays": ['icontains'],
        }


class VolFilter(django_filters.FilterSet):
    class Meta:
        model = Vol
        fields = {
            "avion": ['exact'],
            "depart": ['exact'],
            "arrive": ['exact'],
            "heure_depart": ['gte', 'lte'],
            "duree": ['gte', 'lte'],
            "jours": ['exact'],
        }


class EscaleFilter(django_filters.FilterSet):
    class Meta:
        model = Escale
        fields = {
            "vol": ['exact'],
            "ville": ['exact'],
            "heure_arrive": ['gte', 'lte'],
            "duree": ['gte', 'lte'],
            "no_ord": ['gte', 'lte'],
        }