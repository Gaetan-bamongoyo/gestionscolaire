from django.shortcuts import render, redirect
from .models import *
from scolaireapp.models import *

# Create your views here.
def homePage(request):
    get_classe = Classes.objects.all()
    get_annee = AnneeAcademiques.objects.all()
    get_cours = Cours.objects.all()
    get_enseignant = Enseignants.objects.all()
    get_cours_affecter = []

    for i in get_cours:
        data = Affectations.objects.filter(cours = i.id).exists()
        if data:
            continue

        get_cours_affecter.append({
            "cours": i.designation,
            "id": i.id
        })

    get_affectation = []
    for e in get_enseignant:
        data = Affectations.objects.filter(enseignant = e)
        get_affectation.append({
            "enseignant": e.noms,
            "cours": [
                {
                    "cours": a.cours.designation,
                    "classe": a.cours.classe.classe,
                    "id": a.cours.id
                } for a in data
            ]
        })
    context = {
        'classe': get_classe,
        'annee': get_annee,
        'cours': get_cours,
        'enseignant': get_enseignant,
        'affectation': get_affectation,
        'cours_affecte': get_cours_affecter
    }
    return render(request, 'cours/home.html', context)

def pointpage(request, pk):
    get_cours = Cours.objects.get(id = pk)
    classe = get_cours.classe
    get_eleve = Inscriptions.objects.filter(classe = classe)
    get_all_ponderation = Ponderations.objects.filter(cours = pk)

    get_eleve_point = []
    for item in get_all_ponderation:
        item.echec = item.point_obtenu < (item.cours.ponderation / 2)

    for item in get_eleve:
        id = item.eleve
        deja_cote = Ponderations.objects.filter(eleve = id, cours = pk).exists()

        if deja_cote:
            continue

        get_eleve_point.append({
            "nom": item.eleve.nom,
            "id": item.eleve.id
        })
    return render(request, 'cours/notation.html', {'eleve':get_eleve_point, 'point':get_all_ponderation, 'pk':pk})

def createCours(request):
    if request.method == 'POST':
        data = request.POST
        get_designation = data.get('designation')
        get_classe = data.get('classe')
        get_classe_id = Classes.objects.get(id = get_classe)
        get_classe_id.id
        get_ponderation = data.get('ponderation')

        Cours.objects.create(
            designation = get_designation,
            classe = get_classe_id,
            ponderation = get_ponderation
        )
        return redirect('cours')

def createEnseignant(request):
    if request.method == 'POST':
        data = request.POST
        get_noms = data.get('nom')
        get_prenom = data.get('prenom')
        get_sexe = data.get('sexe')
        get_datenaissance = data.get('datenaissance')
        get_lieunaissance = data.get('lieu')
        get_grade = data.get('grade')
        get_etatcivil = data.get('etat')

        Enseignants.objects.create(
            noms = get_noms,
            prenom = get_prenom,
            sexe = get_sexe,
            datenaissance = get_datenaissance,
            lieunaissance = get_lieunaissance,
            grade = get_grade,
            etatcivil = get_etatcivil
        )
        return redirect('cours')

def createAffectation(request):
    if request.method == 'POST':
        data = request.POST
        get_enseignant = data.get('enseignant')
        get_enseignant_id = Enseignants.objects.get(id = get_enseignant)
        get_enseignant_id.id
        get_cours = data.get('cours')
        get_cours_id = Cours.objects.get(id = get_cours)
        get_cours_id.id
        get_annee = data.get('annee')
        get_annee_id = AnneeAcademiques.objects.get(id = 1)
        get_annee_id.id

        Affectations.objects.create(
            enseignant = get_enseignant_id,
            cours = get_cours_id,
            annee = get_annee_id
        )
        return redirect('cours')

def createPonderations(request, pk):
    if request.method == 'POST':
        data = request.POST
        get_cours = Cours.objects.get(id = pk)
        get_cours.id
        get_eleve = data.get('eleve')
        get_eleve_id = Eleves.objects.get(id = get_eleve)
        get_eleve_id.id
        get_point = data.get('point')
        get_periode = data.get('periode')
        get_annee = data.get('1')
        get_annee_id = AnneeAcademiques.objects.get(id = 1)
        get_annee_id.id

        Ponderations.objects.create(
            point_obtenu = get_point,
            eleve = get_eleve_id,
            cours = get_cours,
            periode = get_periode,
            annee = get_annee_id
        )
        url = f'/cours/point/{pk}'
        return redirect(url)
