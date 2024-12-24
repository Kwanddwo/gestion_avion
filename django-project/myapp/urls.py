from django.urls import path
from . import views
from . import simulations

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("vol", views.vol, name="vol"),
    path("vol/<int:pk>", views.vol_view, name="vol_view"),
    path("escale/create/<int:vol_pk>", views.create_escale, name="create_escale"),
    path("escale/<int:pk>", views.escale, name="escale"),
    path("avion", views.avion, name="avion"),
    path("avion/<int:pk>", views.avion_view, name="avion_view"),
    path('employe/', views.employe, name='employe'),
    path('employe/<int:pk>/', views.employe_view, name='employe_view'),
    path('employe_navigant/<int:pk>/', views.employe_navigant_view, name='employe_navigant_view'),
    path('rapport/', views.rapport, name='rapport'),
    path('rapport/<int:pk>/', views.rapport_view, name='rapport_view'),
    path('ville/', views.ville, name='ville'),
    path('ville/<int:pk>/', views.ville_view, name='ville_view'),

    path('simulate/mois/', simulations.simulateMois, name="simulate_mois"),
    path('simulate/vol/<int:pk>', simulations.simulateVol, name="simulate_vol"),
]