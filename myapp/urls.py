from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    
    #Rapports Gestion
    path('rapports/', views.liste_rapports, name='liste_rapports'),
    path('add-rapport/', views.add_rapport, name='add_rapport'),
    path('modifier_rapport/', views.modifier_rapport, name='modifier_rapport'),
    path('delete-rapport/<int:rapport_id>/', views.delete_rapport, name='delete_rapport'),
    
    #Gestion Employe
    path('employes/', views.liste_employes, name='liste_employes'),
    path('modifier_employe/', views.modifier_employe, name='modifier_employe'),
    path("add-employe/", views.add_employe, name="add_employe"),
    path("delete-employe/<int:employe_id>/", views.delete_employe, name="delete_employe"),
    
    #Gestion Des Navigants
    path('employes-navigants/', views.liste_employes_navigants, name='liste_employes_navigants'),
    path('modifier-employe-navigant/', views.modifier_employe_navigant, name='modifier_employe_navigant'),
    path('add-employe-navigant/', views.add_employe_navigant, name='add_employe_navigant'),
    path('delete-employe-navigant/<int:employe_navigant_id>/', views.delete_employe_navigant, name='delete_employe_navigant'),
    
    #Gestion Ville
    path('villes/', views.liste_villes, name='liste_villes'),
    path('modifier-ville/', views.modifier_ville, name='modifier_ville'),
    path('add-ville/', views.add_ville, name='add_ville'),
    path('delete-ville/<int:ville_id>/', views.delete_ville, name='delete_ville')
]