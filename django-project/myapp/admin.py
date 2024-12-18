from django.contrib import admin
from .models import User, Avion, Rapport, Employe, EmployeNavigant, Ville, Jour, Vol, Escale

# Register your models here.
admin.site.register(User)
admin.site.register(Avion)
admin.site.register(Rapport)
admin.site.register(Employe)
admin.site.register(EmployeNavigant)
admin.site.register(Ville)
admin.site.register(Jour)
admin.site.register(Vol)
admin.site.register(Escale)

