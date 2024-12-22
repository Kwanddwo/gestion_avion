from django.urls import path
from . import views

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
    path('employe_navigant/', views.employe_navigant, name='employe_navigant'),
    path('employe_navigant/<int:pk>/', views.employe_navigant_view, name='employe_navigant_view'),
    path('rapport/', views.rapport, name='rapport'),
    path('rapport/<int:pk>/', views.rapport_view, name='rapport_view'),
    path('ville/', views.ville, name='ville'),
    path('ville/<int:pk>/', views.ville_view, name='ville_view')
]