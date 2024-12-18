from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # shows all vols
    path('login', views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("vol", views.vol, name="vol"),
    path("vol/<int:pk>", views.vol_view, name="vol_view"),
    path("avion", views.avion, name="avion"),
    path("rapport", views.rapport, name="rapport"),
    path("employe", views.employe, name="employe"),
    path("ville", views.ville, name="ville")
]