from django.contrib import admin
from .models import User, Avion, Rapport, Employe, EmployeNavigant, Ville, Jour, Vol, Escale

# Register the User model
admin.site.register(User)

# Customize Avion model admin
@admin.register(Avion)
class AvionAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_avion', 'date_mise_service', 'heures_vol_der_rev', 'heures_vol', 'date_der_rev')
    search_fields = ('type_avion',)
    list_filter = ('date_mise_service', 'date_der_rev')

# Customize Rapport model admin
@admin.register(Rapport)
class RapportAdmin(admin.ModelAdmin):
    list_display = ('id', 'avion', 'texte', 'heures_vol', 'date')
    search_fields = ('texte',)
    list_filter = ('date',)

# Customize Employe model admin
@admin.register(Employe)
class EmployeAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'prenom', 'is_navigant', 'date_embauche')
    search_fields = ('nom', 'prenom')
    list_filter = ('is_navigant', 'date_embauche')

# Customize EmployeNavigant model admin
@admin.register(EmployeNavigant)
class EmployeNavigantAdmin(admin.ModelAdmin):
    list_display = ('id', 'employe', 'heures_vol', 'heures_mois_vol')
    search_fields = ('employe__nom', 'employe__prenom')
    list_filter = ('heures_vol',)

# Customize Ville model admin
@admin.register(Ville)
class VilleAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'nom_pays')
    search_fields = ('nom', 'nom_pays')

# Customize Jour model admin
@admin.register(Jour)
class JourAdmin(admin.ModelAdmin):
    list_display = ('id', 'jour')
    search_fields = ('jour',)

# Customize Vol model admin
@admin.register(Vol)
class VolAdmin(admin.ModelAdmin):
    list_display = ('id', 'avion', 'depart', 'arrive', 'heure_depart', 'duree')
    search_fields = ('avion__type_avion', 'depart__nom', 'arrive__nom')
    list_filter = ('heure_depart', 'duree')

# Customize Escale model admin
@admin.register(Escale)
class EscaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'vol', 'ville', 'heure_arrive', 'duree', 'no_ord')
    search_fields = ('vol__id', 'ville__nom')
    list_filter = ('heure_arrive', 'duree')
