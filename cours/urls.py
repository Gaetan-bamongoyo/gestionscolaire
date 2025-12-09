from django.urls import *
from .views import *

urlpatterns = [
    path('', homePage, name='cours'),
    path('createcours', createCours, name='createcours'),
    path('createenseignant', createEnseignant, name='createenseignant'),
    path('createaffectation', createAffectation, name='createaffectation'),
    path('createpoint/<int:pk>', createPonderations, name='createpoint'),
    path('point/<int:pk>', pointpage, name='point')
]
