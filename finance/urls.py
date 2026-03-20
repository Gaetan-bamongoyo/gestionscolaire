from django.urls import path
from .views import *

urlpatterns = [
    path('comptabilite/', comptabilitePage, name='comptabilite'),
    path('create_frais', create_frais, name='create_frais'),
    path('create_repartition', create_repartition_frais, name='create_repartition'),
    path('recherche_frais_repartition/', recherche_frais_repartition, name='recherche_frais_repartition'),
    path('recherche_eleve/', recherche_eleve, name='recherche_eleve'),
    path('recherche_frais_classe/', recherche_frais_classe, name='recherche_frais_classe')
]