from django.urls import path
from .views import *

urlpatterns = [
    path('classe', classePage, name='classe'),
    path('enregistrement', enregistreInscription, name='enregistrement'),
    path('recherche_parent/', rechercheParent, name='recherche_parent'),
    path('recherche_eleve/', rechercheEleve, name='recherche_eleve'),
    path('setting', settingPage, name='setting'),
    path('inscription', inscriptionPage, name='inscription'),
    path('nouvelle_classe', saveClasse, name='nouvelle_classe'),
    path('nouvelle_annee', create_annee, name='nouvelle_annee'),
    path('modifier_page/<str:id>', modifierPage, name='modifier_page'),
    path('modifier_eleve', modifierEleve, name='modifier_eleve'),
    path('nouvelle_option', create_option, name='nouvelle_option'),
]