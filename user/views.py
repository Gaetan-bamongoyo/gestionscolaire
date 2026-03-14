from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from scolaireapp.models import *

# Create your views here.

def create_ecole(request):
    if request.method == 'POST':
        data = request.POST
        get_nomecole = data.get('nom_ecole')
        get_adresseecole = data.get('adresse_ecole')
        get_telephoneecole = data.get('telephone_ecole')
        get_emailecole = data.get('email_ecole')
        get_arreteministerielecole = data.get('arreteministeriel_ecole')
        get_datecreationecole = data.get('datecreation_ecole')

        create_ecole = Ecole.objects.get(nom = get_nomecole)
        if create_ecole is not None:
            return create_ecole.id
        else:
            create_ecole = Ecole.objects.create(
                nom = get_nomecole,
                adresse = get_adresseecole,
                telephone = get_telephoneecole,
                email = get_emailecole,
                arreteministeriel = get_arreteministerielecole,
                datecreation = get_datecreationecole
            )
            return create_ecole.id

def create_section(request):
    if request.method == 'POST':
        data = request.POST
        get_section = data.get('section')
        ecole = create_ecole(request)


        create_section = Section.objects.create(
            section = get_section,
            ecole_id = ecole
        )
        return create_section.id

def create_user(request):
    if request.method == 'POST':
        data = request.POST
        get_username = data.get('username')
        get_password = data.get('password')

        # recuperer ou creer une ecole et recuperer son id
        get_nomecole = data.get('nom_ecole')
        get_adresseecole = data.get('adresse_ecole')
        get_telephoneecole = data.get('telephone_ecole')
        get_emailecole = data.get('email_ecole')
        get_arreteministerielecole = data.get('arreteministeriel_ecole')
        get_datecreationecole = data.get('datecreation_ecole')
        create_ecole = Ecole.objects.create(
            nom = get_nomecole,
            adresse = get_adresseecole,
            telephone = get_telephoneecole,
            email = get_emailecole,
            arreteministeriel = get_arreteministerielecole,
            datecreation = get_datecreationecole
        )
        # create_ecole.id

        # recuperer ou creer la section et recuperer son id
        section = create_section(request)

        # creer le compte utilisateur et recuperer son id
        create_user = Utilisateurs.objects.create_user(
            username = get_username,
            password = get_password,
            role = "super-admin",
            email = get_emailecole,
            ecole_id = create_ecole.id,
            section_id = section
        )
        
        # l'utilisateur est automatiquement connecté après sa création
        login(request, create_user)
        return redirect('dashboard')

def loginUser(request):
    if request.method == 'POST':
        data = request.POST
        get_username = data.get('username')
        get_password = data.get('password')

        user = authenticate(request, username=get_username, password=get_password)
        print(user)

        if user is not None:
            login(request, user)
            if user.role == 'super_admin':
                return redirect('dashboard')
            elif user.role == 'promoteur':
                return redirect('dashboard_user')
            elif user.role == 'enseignant':
                return redirect('dashboard_caisse')
            else:
                return redirect('dashboard')
        else:
            return redirect('login')
    else:
        return redirect('login')

def logoutPage(request):
    logout(request)
    return redirect('login')

@login_required
def dashboardPage(request):
    if request.user.is_authenticated:
        section = request.user.section
        annee = AnneeScolaires.objects.filter(ecole = request.user.ecole, is_active = True).first()
        return render(request, 'dashboard.html', {'section':section, 'annee':annee})

def loginPage(request):
    return render(request, 'login.html')

def create_compte_page(request):
    return render(request, 'create_compte.html')

@login_required
def nouveau_utilisateur(request):
    if request.user.is_authenticated:

        # recuperation de l'ecole et section
        ecole = request.user.ecole
        section = request.user.section
        

        if request.method == 'POST':
            data = request.POST
            get_username = data.get('user_username')
            get_password = data.get('user_password')
            get_role = data.get('user_role')
            get_email = data.get('user_email')
            get_section_id = data.get('user_section')
            get_nom = data.get('user_nom')

            # Recuperer la section cible (celle choisie dans le formulaire)
            try:
                target_section = Section.objects.get(id=get_section_id)
            except (Section.DoesNotExist, ValueError):
                return JsonResponse({
                    'success': False,
                    'message': 'Section invalide.'
                })

            # verifier si l'utilisateur existe deja
            if Utilisateurs.objects.filter(username = get_username).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'Un utilisateur avec ce nom d\'utilisateur existe deja.'
                })
            
            # verifier si l'email existe deja
            if Utilisateurs.objects.filter(email = get_email).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'Un utilisateur avec ce email existe deja.'
                })
            
            # verifier si le role super-admin par rapport a la section existe deja
            if get_role == 'super-admin' and Utilisateurs.objects.filter(role = 'super-admin', section = target_section, ecole = ecole).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'Un super-admin existe déjà pour cette section.'
                })

            # enregistrement de nouveau utilisateur
            Utilisateurs.objects.create_user(
                username = get_username,
                password = get_password,
                role = get_role,
                email = get_email,
                ecole = ecole,
                section = target_section,
                first_name = get_nom
            )
            return JsonResponse({
                'success': True,
                'message': 'Utilisateur enregistré avec succès.'
            })

@login_required
def update_ecole(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            data = request.POST
            get_nom = data.get('nom_ecole')
            get_adresse = data.get('adresse_ecole')
            get_telephone = data.get('telephone_ecole')
            get_email = data.get('email_ecole')
            get_arreteministeriel = data.get('arreteministeriel_ecole')
            get_datecreation = data.get('datecreation_ecole')
            get_logo = request.FILES.get('logo_ecole')
            
            # recuperer l'ecole de l'utilisateur
            ecole = request.user.ecole
            
            # mettre a jour les informations
            ecole.nom = get_nom
            ecole.adresse = get_adresse
            ecole.telephone = get_telephone
            ecole.email = get_email
            ecole.arreteministeriel = get_arreteministeriel
            ecole.datecreation = get_datecreation
            if get_logo:
                ecole.logo = get_logo
            ecole.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Ecole mise à jour avec succès.'
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Une erreur est survenue.'
            })