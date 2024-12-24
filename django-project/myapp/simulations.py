from django.shortcuts import get_list_or_404, get_object_or_404, redirect

from .models import Vol, EmployeNavigant

def simulateVol(request, pk):
    vol = get_object_or_404(Vol, pk=pk)
    avion = vol.avion
    avion.add_heures_vol(vol)
    avion.save()
    equipe = avion.equipe.all()
    for employeNav in equipe:
        employeNav.add_heures_vol(vol)
        employeNav.save()

    return redirect("vol_view", pk)

def simulateMois(request):
    employesNav = EmployeNavigant.objects.all()
    for empNav in employesNav:
        empNav.heures_mois_vol = 0
        empNav.save()
    
    return redirect("employe")