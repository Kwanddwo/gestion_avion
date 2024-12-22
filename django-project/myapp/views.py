from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.exceptions import ValidationError
import datetime

from .models import User, Vol, Escale, Avion, Employe, EmployeNavigant, Rapport, Ville
from .forms import VolForm, EscaleForm, AvionForm, EmployeForm, EmployeNavigantForm, RapportForm, VilleForm

# TODO: remove csrf_exempt later

@login_required
def index(request):
    return render(request, 'myapp/index.html')

@csrf_exempt
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "myapp/login.html", {
                "message": "Invalid username and/or password."
            })

    return render(request, "myapp/login.html")

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")

@csrf_exempt
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"] 

        # Ensure password is not empty
        if not password:
            return render(request, "myapp/register.html", {
                "message": "Password cannot be empty."
            })
        
        # Ensure password matches confirmation
        if password != confirmation:
            return render(request, "myapp/register.html", {
                "message": "Passwords must match."
            })
 
        # Attempt to create new user
        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()
        except IntegrityError:
            return render(request, "myapp/register.html", {
                "message": "Username already taken."
            })
        
        # Log the user in
        login(request, user)  
  
        return redirect("index")

    return render(request, "myapp/register.html")

@login_required
@csrf_exempt
def vol(request):
    createForm = VolForm()

    if request.method == "POST":
        createForm = VolForm(request.POST)
        createForm.save()
    
    vols = Vol.objects.all()
    return render(request, "myapp/vols.html", {
        "vols": vols, 
        "createForm": createForm,
    })

@login_required
@csrf_exempt
def vol_view(request, pk):
    vol = get_object_or_404(Vol, pk=pk)    

    if request.method == "POST":
        if request.POST.get("_method") == "DELETE":
            vol.delete()
            return redirect("vol")
        
        updateForm = VolForm(request.POST, instance=vol)
        updateForm.save()
    else:
        updateForm = VolForm(instance=vol)

    escales = vol.escales.all().order_by('no_ord')
    createEscaleForm = EscaleForm()

    return render(request, "myapp/vol_view.html", {
        "vol": vol,
        "escales": escales,
        "updateForm": updateForm,
        "escaleForm": createEscaleForm,
    })
    
@login_required
@csrf_exempt
def create_escale(request, vol_pk):
    vol = get_object_or_404(Vol, pk=vol_pk)

    if request.method == "POST":
        form = EscaleForm(request.POST)
        escale = form.save(commit=False)
        escale.vol = vol
        if escale.ville == vol.depart or escale.ville == vol.arrive:
            raise ValidationError({"ville": "Ville de l'escale est déja le départ ou l'arrivé de ce vol."})
        escale.save()

    return redirect("vol_view", pk=vol_pk)

@login_required
@csrf_exempt
def escale(request, pk):
    escale = get_object_or_404(Escale, pk=pk)
    
    if request.method == "POST":
        if request.POST.get("_method") == "DELETE":
            escale.delete()
            return redirect("vol_view", pk=escale.vol.pk)
        
        form = EscaleForm(request.POST, instance=escale)
        form.save()
        return redirect("vol_view", pk=escale.vol.pk)
    
    form = EscaleForm(instance=escale)
    return render(request, "myapp/escale_edit.html", {
        "escale": escale,
        "form": form,
    })

@login_required
@csrf_exempt
def avion(request):
    createForm = AvionForm()

    if request.method == "POST":
        createForm = AvionForm(request.POST)
        createForm.save()
    
    avions = Avion.objects.all()
    return render(request, "myapp/avions.html", {
        "avions": avions, 
        "createForm": createForm,
    })

@login_required
@csrf_exempt
def avion_view(request, pk):
    # avion = Avion.object.get()
    avion = get_object_or_404(Avion, pk=pk)    

    if request.method == "POST":
        if request.POST.get("_method") == "DELETE":
            avion.delete()
            return redirect("avion")
        
        updateForm = AvionForm(request.POST, instance=avion)
        updateForm.save()
    else:
        updateForm = AvionForm(instance=avion)

    if avion:
        return render(request, "myapp/avion_view.html", {
            "avion": avion,
            "updateForm": updateForm,
        })
    pass


@login_required
@csrf_exempt
#change crete_form
#change list
def employe(request):
    createForm = EmployeForm()

    if request.method == "POST":
        createForm = EmployeForm(request.POST)
        employe = createForm.save()
        if employe.is_navigant:
            EmployeNavigant.objects.create(employe=employe)

    employes = Employe.objects.all()
    return render(request, "myapp/employes.html", {
        "employes": employes,
        "createForm": createForm
    })

@login_required
@csrf_exempt
#change the root name
def employe_view(request, pk):
    employe = get_object_or_404(Employe, pk=pk)

    if request.method == "POST":
        if request.POST.get("_method") == "DELETE":
            employe.delete()
            return redirect("employe")

        updateForm = EmployeForm(request.POST, instance=employe)
        if updateForm.is_valid():
            updateForm.save()
    else:
        updateForm = EmployeForm(instance=employe)

    if employe.is_navigant:
        empNav = EmployeNavigant.objects.get(employe=employe)
        updateNavigantForm = EmployeNavigantForm(instance=empNav)

    return render(request, "myapp/employe_view.html", {
        "employe": employe,
        "updateForm": updateForm,
        "updateNavigantForm": updateNavigantForm if employe.is_navigant else "",
        "employe_navigant": empNav if employe.is_navigant else "", 
    })

@login_required
@csrf_exempt
def employe_navigant_view(request, pk):
    employe_navigant = get_object_or_404(EmployeNavigant, employe__pk=pk)

    if request.method == "POST":
        updateForm = EmployeNavigantForm(request.POST, instance=employe_navigant)
        if updateForm.is_valid():
            updateForm.save()
    
    return redirect("employe_view", pk)

@login_required
@csrf_exempt
def rapport(request):
    createForm = RapportForm()

    if request.method == "POST":
        createForm = RapportForm(request.POST)
        if createForm.is_valid():
            form = createForm.save(commit=False)
            av = form.avion
            form.heures_vol = av.heures_vol
            av.heures_vol_der_rev = 0
            av.date_der_rev = datetime.date.today()
            av.save()
            form.save()

    rapports = Rapport.objects.all()
    return render(request, "myapp/rapports.html", {
        "rapports": rapports,
        "createForm": createForm
    })

@login_required
@csrf_exempt
def rapport_view(request, pk):
    rapport = get_object_or_404(Rapport, pk=pk)

    if request.method == "POST":
        if request.POST.get("_method") == "DELETE":
            rapport.delete()
            return redirect("rapport")

        updateForm = RapportForm(request.POST, instance=rapport)
        if updateForm.is_valid():
            updateForm.save()
    else:
        updateForm = RapportForm(instance=rapport)

    return render(request, "myapp/rapport_view.html", {
        "rapport": rapport,
        "updateForm": updateForm
    })


@login_required
@csrf_exempt
def ville(request):
    createForm = VilleForm()

    if request.method == "POST":
        createForm = VilleForm(request.POST)
        if createForm.is_valid():
            createForm.save()

    villes = Ville.objects.all()
    return render(request, "myapp/ville.html", {
        "villes": villes,
        "createForm": createForm
    })

@login_required
@csrf_exempt
def ville_view(request, pk):
    ville = get_object_or_404(Ville, pk=pk)

    if request.method == "POST":
        if request.POST.get("_method") == "DELETE":
            ville.delete()
            return redirect("ville")

        updateForm = VilleForm(request.POST, instance=ville)
        if updateForm.is_valid():
            updateForm.save()
    else:
        updateForm = VilleForm(instance=ville)

    return render(request, "myapp/ville_view.html", {
        "ville": ville,
        "updateForm": updateForm
    })
