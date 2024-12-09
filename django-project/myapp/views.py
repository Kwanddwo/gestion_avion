from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User

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
