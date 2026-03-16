import traceback
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import JsonResponse
from datetime import date
from .models import *
from user.models import *
from finance.models import *
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import django.db as transaction

# Create your views here.

@login_required
def rechercheParent(request):
    telephone = request.GET.get('telephone_parent')
    if not telephone:
        return JsonResponse({'exists': False})
    
    parent = Parents.objects.filter(telephone=telephone).first()
    if parent:
        data = {
            'exists': True,
            'id': parent.id,
            'nom': parent.nom,
            'prenom': parent.prenom,
            'profession': parent.profession,
            'telephone': parent.telephone,
            'email': parent.email,
            'adresse': parent.adresse
        }
    else:
        data = {'exists': False}
    return JsonResponse(data)

@login_required
def rechercheEleve(request):
    nom = request.GET.get('nom_eleve')
    postnom = request.GET.get('postnom_eleve')
    prenom = request.GET.get('prenom_eleve')
    class_id = request.GET.get('classe')
    annee_id = request.GET.get('annee')
    
    # Récupérer l'année scolaire (soit par ID, soit l'active de l'école)
    if annee_id:
        annee_scolaire = AnneeScolaires.objects.filter(id=annee_id).first()
    else:
        annee_scolaire = AnneeScolaires.objects.filter(ecole=request.user.ecole, is_active=True).first()

    if not (nom and postnom and prenom and annee_scolaire):
        return JsonResponse({'exists': False})

    eleve = Eleves.objects.filter(nom=nom, postnom=postnom, prenom=prenom).first()
    if eleve:
        # Vérifier s'il y a une inscription pour cet élève, cette classe et cette année
        query = Inscriptions.objects.filter(eleve=eleve, annee=annee_scolaire)
        if class_id:
            query = query.filter(classe_id=class_id)
        
        inscription = query.first()
        if inscription:
            data_eleve = { 
                'exists': True, 
                'id': eleve.id, 
                'nom': eleve.nom, 
                'postnom': eleve.postnom, 
                'prenom': eleve.prenom, 
                'classe': inscription.classe.classe, 
                'annee': inscription.annee.annee, 
            } 
        else:
            data_eleve = {'exists': False}
    else:
        data_eleve = {'exists': False}
    return JsonResponse(data_eleve)

@login_required
def create_or_return_parent_id(request):
    if request.method == 'POST':
        id = request.POST.get('id_parent')
        if id:
            try:
                parent = Parents.objects.get(id=id)
                return parent.id
            except Parents.DoesNotExist:
                pass
        else:
            nom = request.POST.get('nom_parent')
            prenom = request.POST.get('prenom_parent')
            profession = request.POST.get('profession_parent')
            email = request.POST.get('email_parent')
            adresse = request.POST.get('adresse_parent')
            telephone = request.POST.get('telephone_parent')

            parent, created = Parents.objects.get_or_create(
                nom=nom,
                prenom=prenom,
                profession=profession,
                email=email,
                adresse=adresse,
                telephone=telephone
            )
            return parent.id

@login_required
def inscriptionPage(request):
    if request.user.is_authenticated:
        ecole = request.user.ecole
        section = request.user.section
        get_annee = AnneeScolaires.objects.filter(is_active=True, ecole=ecole) 

        # Afficher les classes en fonction de la section de l'école
        get_classe = Classes.objects.filter(section = section, section__ecole = ecole, is_active=True)

        get_option = Options.objects.all()

        data = {
            'annee': get_annee,
            'classe': get_classe,
            'option': get_option,
            'section': section
        }
        return render(request, 'eleves/eleve.html', data)

@login_required
def enregistreInscription(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            data = request.POST

            # recuperer ou creer le parent et recuperer son id
            get_parent_id = create_or_return_parent_id(request)
            parent = Parents.objects.get(id=get_parent_id)
            parent.id

            # recuperer les informations de l'eleve
            get_nomeleve = data.get('nom_enfant')
            get_postnomeleve = data.get('postnom_enfant')
            get_prenomeleve = data.get('prenom_enfant')
            get_sexe = data.get('sexe')
            get_lieunaissance = data.get('lieu_enfant')
            get_datenaissance = data.get('date_enfant')
            get_telephoneeleve = data.get('telephone_enfant')
            get_adresseeleve = data.get('adresse_enfant')
            get_photo = request.FILES.get('photo')
            
            # creer l'eleve
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

            # recuperer les informations de l'inscription
            get_classe = data.get('classe')
            get_classe_id = Classes.objects.get(id = get_classe)
            get_classe_id.id
            get_annee = AnneeScolaires.objects.get(is_active = True)

            # recuperer la section de l'ecole pour verifier si c'est secondaire ou pas
            ecole = request.user.ecole
            section = request.user.section

            # verifier si l'eleve est deja inscrit pour eviter les doublons
            if Inscriptions.objects.filter(eleve = get_eleve.id, annee = get_annee).exists():
                return redirect('inscription')
            
            Inscriptions.objects.create(
                classe = get_classe_id,
                eleve = get_eleve,
                annee = get_annee,
            )
            return redirect('classe')
            
        else:
            return redirect('eleve')

@login_required
def settingPage(request):
    if request.user.is_authenticated:
        # recuperer la section enregistrer deja
        section_possible = [
            "Primaire","Secondaire","Maternelle"
        ]
        sections_enregistrees = Section.objects.values_list('section', flat=True)
        sections_disponible = [
            section for section in section_possible if section not in sections_enregistrees
        ]

        # recuperer les roles enregistrer deja
        role_disponible = [
            "enseignant","controleur","comptable","secretaire", "super-admin","admin"
        ]

        # recuperer les sections de l'ecole
        get_sections = Section.objects.filter(ecole = request.user.ecole)
        
        # recuperer les utilisateurs
        get_users = Utilisateurs.objects.filter(ecole = request.user.ecole)
        get_classe = Classes.objects.filter(section = request.user.section, is_active=True)
        get_annee = AnneeScolaires.objects.filter(ecole = request.user.ecole)
        # recuperer les informations de l'ecole
        get_ecole = request.user.ecole

        get_frais = Frais.objects.filter(ecole = get_ecole, section = request.user.section )
        get_repartition = RepartitionFrais.objects.filter(ecole = get_ecole, section = request.user.section).order_by('frais__classe__classe')
        get_options = Options.objects.filter(ecole = get_ecole) 

        context = {
            'section':sections_disponible,
            'users':get_users,
            'classes':get_classe,
            'annee': get_annee,
            'ecole': get_ecole,
            'roles': role_disponible,
            'sections': get_sections,
            'list_frais': get_frais,
            'repartition_frais':get_repartition,
            'options': get_options,
            'liste_section':get_sections
        }
        return render(request, 'setting.html', context)

@login_required
def saveClasse(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            data = request.POST
            get_classe = data.get('classe_nom')
            get_id = data.get('id_classe')
            get_is_active = True if data.get('is_active') == 'on' else False
            get_option = data.get('option_classe')

            # recuperer l'id de l'option (optionnel)
            get_option_id = None
            if get_option:
                try:
                    get_option_id = Options.objects.get(id = get_option)
                except (Options.DoesNotExist, ValueError):
                    pass

            # recuperer la section de l'ecole pour verifier si c'est secondaire ou pas
            section = request.user.section

            # recuperer l'ecole de l'utilisateur pour l'associer a la classe
            ecole = request.user.ecole

            # verification si l'id existe pour mise à jour
            if get_id and get_id != '':
                try:
                    get_classe_id = Classes.objects.get(id = get_id, ecole = ecole)
                    get_classe_id.classe = get_classe
                    get_classe_id.is_active = get_is_active
                    get_classe_id.option = get_option_id
                    get_classe_id.save()
                    return JsonResponse({
                        'success': True,
                        'message': 'Classe mise à jour avec succès.'
                    })
                except (Classes.DoesNotExist, ValueError):
                    pass # Si l'ID est invalide, on continue comme une nouvelle création ou on renvoie une erreur
            
            # Vérification d'existence pour une nouvelle classe ou si la mise à jour a échoué
            if Classes.objects.filter(classe = get_classe, section = section, ecole = ecole, option = get_option_id).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'La classe existe deja.'
                })

            else:
                Classes.objects.create(
                    classe = get_classe,
                    section = section,
                    ecole = ecole,
                    is_active = get_is_active,
                    option = get_option_id
                )
                return JsonResponse({
                    'success': True,
                    'message': 'Classe enregistrée avec succès.'
                })

@login_required
def create_annee(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            data = request.POST
            get_id = data.get('id_annee')
            get_annee = data.get('annee_nom')

            # recuperer l'ecole de l'utilisateur pour l'associer a l'annee academique
            ecole = request.user.ecole

            if AnneeScolaires.objects.filter(annee = get_annee, ecole = ecole).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'L\'annee scolaire existe deja.'
                })

            if get_id:
                AnneeScolaires.objects.filter(ecole=ecole).update(is_active=False)

                get_annee_id = AnneeScolaires.objects.get(id = get_id, ecole = ecole)
                get_annee_id.annee = get_annee
                get_annee_id.is_active = True
                get_annee_id.save()
                return JsonResponse({
                    'success': True,
                    'message': 'Annee scolaire mise à jour avec succès.'
                }) 
            
            else:
                # Désactiver les années académiques existantes pour cette école
                AnneeScolaires.objects.filter(ecole=ecole).update(is_active=False)

                # Créer la nouvelle année académique et l'associer à l'école

                AnneeScolaires.objects.create(
                    annee = get_annee,
                    ecole = ecole)
                return JsonResponse({
                    'success': True,
                    'message': 'Annee scolaire mise à jour avec succès.'
                }) 

@login_required
def create_option(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            data = request.POST
            get_id = data.get('id_option')
            get_option = data.get('option_nom')
            # Les checkboxes renvoient 'on' si cochées, sinon elles ne sont pas dans le POST
            get_is_active = True if data.get('is_active') == 'on' else False

            # recuperer l'ecole de l'utilisateur pour l'associer a l'option
            ecole = request.user.ecole

            if get_id:
                # En cas de modification, on vérifie si un AUTRE enregistrement porte le même nom
                if Options.objects.filter(option = get_option, ecole = ecole).exclude(id = get_id).exists():
                    return JsonResponse({
                        'success': False,
                        'message': 'Une autre option avec ce nom existe deja.'
                    })

                get_option_id = Options.objects.get(id = get_id, ecole = ecole)
                get_option_id.option = get_option
                get_option_id.is_active = get_is_active
                get_option_id.save()
                return JsonResponse({
                    'success': True,
                    'message': 'Option mise à jour avec succès.'
                }) 
            
            else:
                if Options.objects.filter(option = get_option, ecole = ecole).exists():
                    return JsonResponse({
                        'success': False,
                        'message': 'L\'option existe deja.'
                    })

                # Créer la nouvelle option et l'associer à l'école
                Options.objects.create(
                    option = get_option,
                    ecole = ecole,
                    is_active = get_is_active
                )
                return JsonResponse({
                    'success': True,
                    'message': 'Option enregistrée avec succès.'
                }) 

@login_required
def classePage(request):
    if request.user.is_authenticated:
        section = request.user.section
        ecole = request.user.ecole
        get_classe = Classes.objects.filter(section = section, section__ecole = ecole, is_active=True)
        annee = AnneeScolaires.objects.filter(is_active = True, ecole = ecole).first()
        print(get_classe)
        
        # Si c'est une requête AJAX pour récupérer les données d'une classe
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            classe_id = request.GET.get('id')
            if classe_id:
                try:
                    # Récupérer la classe par ID pour éviter les doublons de nom
                    classe_obj = Classes.objects.get(id=classe_id, section=section)
                    
                    # Récupérer les inscriptions de cette classe
                    inscriptions = Inscriptions.objects.filter(classe=classe_obj, is_active=True, classe__section__ecole = ecole, annee = annee)
                    print(inscriptions)
                    
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
                            'id': eleve.id,
                            'nom_complet': f"{eleve.nom} {eleve.postnom} {eleve.prenom}",
                            'sexe': eleve.sexe,
                            'age': age,
                            'date_naissance': date_naissance,
                            'lieu_naissance': eleve.lieunaissance,
                            'telephone': eleve.telephone,
                            'adresse': eleve.adresse,
                            'option': inscription.classe.option.option if (inscription.classe and inscription.classe.option) else '-',
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
                    print("ERREUR COMPLETTE:")
                    print(traceback.format_exc())
                    return JsonResponse({'error': str(e)}, status=500)
        
        return render(request, 'classe.html', {'get_classe':get_classe})

@login_required
def modifierPage(request, id):
    get_eleve = Eleves.objects.get(id = id)
    return render(request, 'eleves/modifier.html', {'eleve':get_eleve})

@login_required
def modifierEleve(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            data = request.POST

            # recuperer les informations de parent et enregistrement
            id = data.get('id_parent')
            nom = data.get('nom_parent')
            prenom = data.get('prenom_parent')
            profession = data.get('profession_parent')
            email = data.get('email_parent')
            adresse = data.get('adresse_parent')
            telephone = data.get('telephone_parent')

            parent = Parents.objects.get(id = id)
            Parents.objects.filter(id = id).update(
                nom=nom,
                prenom=prenom,
                profession=profession,
                email=email,
                adresse=adresse,
                telephone=telephone
            )

            
            # recuperer les informations de l'eleve et enregistrement
            get_id_eleve = data.get('id_eleve')
            get_nomeleve = data.get('nom_enfant')
            get_postnomeleve = data.get('postnom_enfant')
            get_prenomeleve = data.get('prenom_enfant')
            get_sexe = data.get('sexe')
            get_lieunaissance = data.get('lieu_enfant')
            get_datenaissance = data.get('date_enfant')
            get_telephoneeleve = data.get('telephone_enfant')
            get_adresseeleve = data.get('adresse_enfant')
            get_photo = request.FILES.get('photo')

            eleve = Eleves.objects.get(id = get_id_eleve)
            
            # Eleves.objects.filter(id = get_id_eleve,).update(
            eleve.nom = get_nomeleve
            eleve.postnom = get_postnomeleve
            eleve.prenom = get_prenomeleve
            eleve.sexe = get_sexe
            eleve.lieunaissance = get_lieunaissance
            eleve.datenaissance = get_datenaissance
            eleve.telephone = get_telephoneeleve
            eleve.adresse = get_adresseeleve
            eleve.photo = get_photo
            eleve.parent = parent
            eleve.save()
            # )
            print(get_datenaissance)
            return redirect('classe')



