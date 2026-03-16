from django.urls import path
from .views import *

urlpatterns = [
    path('', loginPage, name='login'),
    path('create_compte/', create_compte_page, name='create_compte'),
    path('create_user/', create_user, name='create_user'),
    path('logout/', logoutPage, name='logout'),
    path('dashboard/', dashboardPage, name='dashboard'),
    path('login_user/', loginUser, name='login_user'),
    path('nouveau_utilisateur/', nouveau_utilisateur, name='nouveau_utilisateur'),
    path('update_ecole', update_ecole, name='update_ecole'),
    path('nouvelle_section', nouvelle_section, name='nouvelle_section'),
    path('update_profile', update_profile, name='update_profile')
]


