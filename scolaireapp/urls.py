from django.urls import path
from .views import *

urlpatterns = [
    path('', loginPage, name='index'),
    path('login', loginUser, name='login'),
    path('dashboard', dashboardPage, name='dashboard'),
    path('logout', logoutPage, name='logout'),
    path('classe', classePage, name='classe'),
    path('enregistrement', enregistreInscription, name='enregistrement'),
    path('setting', settingPage, name='setting'),
    path('inscription', inscriptionPage, name='inscription'),
    path('saveclasse', saveClasse, name='saveclasse'),
    path('saveniveau', saveNiveau, name='saveniveau')
]