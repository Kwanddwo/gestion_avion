from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.exceptions import ValidationError

from .models import User, Vol, Escale, Avion
from .forms import VolForm, EscaleForm, AvionForm

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
def rapport(request):
    pass

@login_required
def employe(request):
    pass

@login_required
def ville(request):
    pass
