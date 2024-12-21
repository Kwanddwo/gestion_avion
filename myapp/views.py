from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse


from .models import User, Vol, Employe, EmployeNavigant, Rapport, Ville, Avion

# TODO: remove csrf_exempt later


# These all do actions based on the type of request they get
# (GET, POST, PUT, DELETE...)
# GET creates a model, POST creates, PUT updates, DELETE deletes...
# other actions will need another view
# those are my views


@login_required
def index(request):
    return render(request, 'myapp\index.html')

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
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "myapp/login.html", {
                "message": "Invalid username and/or password."
            })

    return render(request, "myapp/login.html")

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

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
  
        return HttpResponseRedirect(reverse("index"))

    return render(request, "myapp/register.html")


@login_required
def liste_employes(request):
    employes = Employe.objects.filter(is_navigant=False) 
    return render(request, 'myapp/liste_employes.html',{
        'employes': employes
    })


@csrf_exempt
def modifier_employe(request):
    if request.method == "POST":
        employe_id = request.POST["id"]
        nom = request.POST["nom"]
        prenom = request.POST["prenom"]

        try:
            employe = Employe.objects.get(pk=employe_id)
            employe.nom = nom
            employe.prenom = prenom
            employe.save()
            return JsonResponse({"success": True, "message": "Modifier l'employe correctement"})
        except Employe.DoesNotExist:
            return JsonResponse({"success": False, "message": "Employee n'exite pas."})
    return JsonResponse({"success": False, "message": "Invalid request."})


@login_required
def add_employe(request):
    if request.method == "POST":
        nom = request.POST["nom"]
        prenom = request.POST["prenom"]

        # Cree nouveau employe
        employe = Employe(nom=nom,
                          prenom=prenom,
                          is_navigant=False)
        employe.save()

        # Return a JSON response avec la data de l'employe
        return JsonResponse({
            "success": True,
            "message": "L'employé a été ajouté avec succès.",
            "id": employe.id,
            "nom": employe.nom,
            "prenom": employe.prenom
        })

@login_required
def delete_employe(request, employe_id):
    if request.method == "DELETE":
        try:
            # on chereche de get l'employe
            employe = Employe.objects.get(id=employe_id)
            employe.delete()
            return JsonResponse({"success": True, "message": "Employé supprimé avec succès."})
        except Employe.DoesNotExist:
            # If l'employe n'exist pas
            return JsonResponse({"success": False, "message": "L'employé n'existe pas."})
    return JsonResponse({"success": False, "message": "Méthode non autorisée."})


#Gestion des Navigant
@login_required
def liste_employes_navigants(request):
    employes_navigants = EmployeNavigant.objects.all()
    avions = Avion.objects.all()
    return render(request, 'myapp/liste_navigants.html', {
        'employes_navigants': employes_navigants,
        'avions': avions
    })

@csrf_exempt
def modifier_employe_navigant(request):
    if request.method == "POST":
        navigant_id = request.POST["id"]
        nom = request.POST["nom"]
        prenom = request.POST["prenom"]
        heures_vol = request.POST["heures_vol"]
        heures_mois_vol = request.POST["heures_mois_vol"]
        avions = request.POST.getlist("avions")

        try:
            employe_navigant = EmployeNavigant.objects.get(id=navigant_id)
            employe_navigant.heures_vol = heures_vol
            employe_navigant.heures_mois_vol = heures_mois_vol
            employe_navigant.avions.set(avions)
            employe_navigant.save()

            employe_navigant.employe.nom = nom
            employe_navigant.employe.prenom = prenom
            employe_navigant.employe.save()

            return JsonResponse({"success": True, "message": "L'employé navigant a été modifié avec succès."})
        except EmployeNavigant.DoesNotExist:
            return JsonResponse({"success": False, "message": "L'employé navigant n'existe pas."})

    return JsonResponse({"success": False, "message": "Requête invalide."})

@login_required
def add_employe_navigant(request):
    if request.method == "POST":
        nom = request.POST["nom"]
        prenom = request.POST["prenom"]
        heures_vol = request.POST["heures_vol"]
        heures_mois_vol = request.POST["heures_mois_vol"]
        avions = request.POST.getlist("avions")

        employe = Employe(nom=nom, prenom=prenom, is_navigant=True)
        employe.save()

        employe_navigant = EmployeNavigant(employe=employe, heures_vol=heures_vol, heures_mois_vol=heures_mois_vol)
        employe_navigant.save()
        employe_navigant.avions.set(avions)
        employe_navigant.save()

        return JsonResponse({
            "success": True,
            "message": "L'employé navigant a été ajouté avec succès.",
            "id": employe_navigant.id,
            "nom": employe_navigant.employe.nom,
            "prenom": employe_navigant.employe.prenom,
            "heures_vol": employe_navigant.heures_vol,
            "heures_mois_vol": employe_navigant.heures_mois_vol,
            "avions": [avion.type_avion for avion in employe_navigant.avions.all()]
        })

@login_required
def delete_employe_navigant(request, employe_navigant_id):
    if request.method == "DELETE":
        try:
            employe_navigant = EmployeNavigant.objects.get(id=employe_navigant_id)
            employe_navigant.delete()
            return JsonResponse({"success": True, "message": "Employé navigant supprimé avec succès."})
        except EmployeNavigant.DoesNotExist:
            return JsonResponse({"success": False, "message": "L'employé navigant n'existe pas."})



# Gestion des Rapports
@login_required
def liste_rapports(request):
    avions = Avion.objects.all()
    rapports = Rapport.objects.all()
    return render(request, 'myapp/liste_rapports.html', {
        'rapports': rapports,
        'avions': avions
    })

@csrf_exempt
def modifier_rapport(request):
    if request.method == "POST":
        rapport_id = request.POST["id"]
        texte = request.POST["texte"]
        heures_vol = request.POST["heures_vol"]

        try:
            rapport = Rapport.objects.get(pk=rapport_id)
            rapport.texte = texte
            rapport.heures_vol = heures_vol
            rapport.save()
            return JsonResponse({"success": True, "message": "Rapport modifié avec succès"})
        except Rapport.DoesNotExist:
            return JsonResponse({"success": False, "message": "Le rapport n'existe pas"})
    return JsonResponse({"success": False, "message": "Requête invalide"})

@login_required
def add_rapport(request):
    if request.method == "POST":
        avion_id = request.POST["avion"]
        texte = request.POST["texte"]
        heures_vol = request.POST["heures_vol"]

        try:
            avion = Avion.objects.get(id=avion_id)
        except Avion.DoesNotExist:
            return JsonResponse({"success": False, "message": "L'avion n'existe pas"})

        # Create new rapport
        rapport = Rapport(avion=avion, texte=texte, heures_vol=heures_vol)
        rapport.save()

        return JsonResponse({
            "success": True,
            "message": "Le rapport a été ajouté avec succès.",
            "id": rapport.id,
            "avion": avion.type_avion,
            "texte": rapport.texte,
            "heures_vol": rapport.heures_vol,
            "date": rapport.date.strftime('%Y-%m-%d')
        })

@login_required
def delete_rapport(request, rapport_id):
    if request.method == "DELETE":
        try:
            rapport = Rapport.objects.get(id=rapport_id)
            rapport.delete()
            return JsonResponse({"success": True, "message": "Rapport supprimé avec succès"})
        except Rapport.DoesNotExist:
            return JsonResponse({"success": False, "message": "Le rapport n'existe pas"})
    return JsonResponse({"success": False, "message": "Méthode non autorisée"})

#Villes Gestion
@login_required
def liste_villes(request):
    villes = Ville.objects.all()
    return render(request, 'myapp/liste_villes.html', {
        'villes': villes
    })


def modifier_ville(request):
    if request.method == "POST":
        ville_id = request.POST.get("id")
        nom = request.POST.get("nom")
        nom_pays = request.POST.get("nom_pays")

        try:
            ville = Ville.objects.get(pk=ville_id)
            ville.nom = nom
            ville.nom_pays = nom_pays
            ville.save()
            return JsonResponse({"success": True, "message": "Ville modifiée avec succès"})
        except Ville.DoesNotExist:
            return JsonResponse({"success": False, "message": "La ville n'existe pas."})
    return JsonResponse({"success": False, "message": "Requête invalide."})

@login_required
def add_ville(request):
    if request.method == "POST":
        nom = request.POST.get("nom")
        nom_pays = request.POST.get("nom_pays")

        # Créer une nouvelle ville
        ville = Ville.objects.create(nom=nom, nom_pays=nom_pays)

        # Retourner une réponse JSON avec les données de la ville
        return JsonResponse({
            "success": True,
            "message": "Ville ajoutée avec succès.",
            "id": ville.id,
            "nom": ville.nom,
            "nom_pays": ville.nom_pays
        })
    return JsonResponse({"success": False, "message": "Requête invalide."})

@login_required
def delete_ville(request, ville_id):
    if request.method == "DELETE":
        try:
            # Rechercher et supprimer la ville
            ville = Ville.objects.get(pk=ville_id)
            ville.delete()
            return JsonResponse({"success": True, "message": "Ville supprimée avec succès."})
        except Ville.DoesNotExist:
            return JsonResponse({"success": False, "message": "La ville n'existe pas."})
    return JsonResponse({"success": False, "message": "Méthode non autorisée."})