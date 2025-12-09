from django.shortcuts import render, redirect
from django.http import JsonResponse
from datetime import date
from .models import *
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

def dashboardPage(request):
    return render(request, 'dashboard.html')

def loginPage(request):
    return render(request, 'login.html')

@login_required
def logoutPage(request):
    logout(request)
    return redirect('login')
    
def loginUser(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')    
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            return redirect('index')
    else:
        return redirect('index')
    
def createuser(request):
    user = User.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(email=email).exists():
                message_erreur = 'Desole le compte existe deja'
                return render(request, 'login/index.html', {'message_erreur':message_erreur})
        else:
                form = User.objects.create_user(
                        username=email,
                        password=password,
                        email=email,
                        is_superuser = 1,
                        first_name=username
                    )
                form.set_password(password)
                form.save()
                user_id = form.id
                retrieved = User.objects.get(id=user_id)
                return render(request, 'login/message.html')

@login_required
def inscriptionPage(request):
    get_annee = AnneeAcademiques.objects.all()
    get_classe = Classes.objects.all()
    get_option = Options.objects.all()

    data = {
        'annee': get_annee,
        'classe': get_classe,
        'option': get_option
    }
    return render(request, 'eleve.html', data)

@login_required
def enregistreInscription(request):
    if request.method == 'POST':
        data = request.POST
        # parent
        get_nomparent = data.get('nom_parent')
        get_prenomparent = data.get('prenoms')
        get_profession = data.get('professions')
        get_telephone = data.get('telephones')
        get_adresse = data.get('adresses')
        parent = Parents.objects.create(
            nom = get_nomparent,
            prenom = get_prenomparent,
            profession = get_profession,
            telephone = get_telephone,
            adresse = get_adresse
        )
        parent.id

        # eleves
        get_nomeleve = data.get('nom_enfant')
        get_postnomeleve = data.get('postnom_enfant')
        get_prenomeleve = data.get('prenom_enfant')
        get_sexe = data.get('sexe')
        get_lieunaissance = data.get('lieu_enfant')
        get_datenaissance = data.get('date_enfant')
        get_telephoneeleve = data.get('telephone_enfant')
        get_adresseeleve = data.get('adresse_enfant')
        get_photo = request.FILES.get('photo')
        
        if Eleves.objects.filter(nom = get_nomeleve, postnom = get_postnomeleve, prenom = get_prenomeleve).exists():
            return redirect('inscription')
        
        get_eleve = Eleves.objects.create(
            nom = get_nomeleve,
            postnom = get_postnomeleve,
            prenom = get_prenomeleve,
            sexe = get_sexe,
            lieunaissance = get_lieunaissance,
            datenaissance = get_datenaissance,
            telephone = get_telephoneeleve,
            adresse = get_adresseeleve,
            photo = get_photo,
            parent = parent
        )
        get_eleve.id

        # inscription
        get_classe = data.get('classe')
        get_classe_id = Classes.objects.get(id = get_classe)
        get_classe_id.id
        get_annee = data.get('annee')
        get_annee_id = AnneeAcademiques.objects.get(id = get_annee)
        get_annee_id.id
        get_option = data.get('option')
        get_option_id = Options.objects.get(id = get_option)
        get_option_id.id

        if Inscriptions.objects.filter(eleve = get_eleve.id, annee = get_annee).exists():
            return redirect('inscription')
        
        Inscriptions.objects.create(
            classe = get_classe_id,
            eleve = get_eleve,
            annee = get_annee_id,
            option = get_option_id
        )
        return redirect('classe')
    else:
        return redirect('eleve')

@login_required
def settingPage(request):
    get_parent = Parents.objects.all()
    get_niveau = Niveaux.objects.all()
    context = {
        'get_parent':get_parent,
        'get_niveau':get_niveau
    }
    return render(request, 'setting.html', context)

@login_required
def saveClasse(request):
    if request.method == 'POST':
        data = request.POST
        get_niveau = data.get('classe_niveau')
        get_niveau_id = Niveaux.objects.get(id = get_niveau)
        get_niveau_id.id
        get_classe = data.get('classe_nom')

        Classes.objects.create(
            niveau = get_niveau_id,
            classe = get_classe
        )
        return redirect('eleve')

@login_required  
def saveNiveau(request):
    if request.method == 'POST':
        data = request.POST
        get_niveau = data.get('niveau')

        Niveaux.objects.create(
            niveau = get_niveau
        )
        return redirect('eleve')

@login_required
def classePage(request):
    get_classe = Classes.objects.all()
    
    # Si c'est une requête AJAX pour récupérer les données d'une classe
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        classe = request.GET.get('classe')
        if classe:
            try:
                # Récupérer la classe
                classe_obj = Classes.objects.get(classe=classe)
                
                # Récupérer les inscriptions de cette classe
                inscriptions = Inscriptions.objects.filter(classe=classe_obj, is_active=True)
                
                # Préparer les données des élèves
                eleves_data = []
                total_filles = 0
                total_garcons = 0
                
                for inscription in inscriptions:
                    eleve = inscription.eleve
                    
                    # Calculer les initiales
                    initials = f"{eleve.nom[0]}{eleve.prenom[0]}"
                    
                    # Compter filles/garçons
                    if eleve.sexe.lower() in ['f', 'femme', 'féminin', 'fille']:
                        total_filles += 1
                    else:
                        total_garcons += 1
                    
                    # Formater la date de naissance
                    date_naissance = eleve.datenaissance.strftime('%d.%m.%Y') if eleve.datenaissance else '-'
                    
                    # Calculer l'âge
                    age = '-'
                    if eleve.datenaissance:
                        today = date.today()
                        age = today.year - eleve.datenaissance.year - ((today.month, today.day) < (eleve.datenaissance.month, eleve.datenaissance.day))
                    
                    eleves_data.append({
                        'initials': initials,
                        'nom_complet': f"{eleve.nom} {eleve.postnom} {eleve.prenom}",
                        'sexe': eleve.sexe,
                        'age': age,
                        'date_naissance': date_naissance,
                        'lieu_naissance': eleve.lieunaissance,
                        'telephone': eleve.telephone,
                        'adresse': eleve.adresse,
                        'option': inscription.option.option if inscription.option else '-',
                        'parent': f"{eleve.parent.nom} {eleve.parent.prenom}"
                    })
                
                # Calculer les statistiques
                total_eleves = len(eleves_data)
                
                # Retourner les données en JSON
                data = {
                    'total': total_eleves,
                    'girls': total_filles,
                    'boys': total_garcons,
                    'students': eleves_data
                }
                
                return JsonResponse(data)
                
            except Classes.DoesNotExist:
                return JsonResponse({'error': 'Classe non trouvée'}, status=404)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
    
    return render(request, 'classe.html', {'get_classe':get_classe})


