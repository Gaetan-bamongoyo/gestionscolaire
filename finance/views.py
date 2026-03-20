from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from scolaireapp.models import *
from .models import *
from django.urls import reverse
from django.db.models import Sum, Q
from django.http import JsonResponse


# Create your views here.

# une fonction qui verifier si le montant que l'utilisateur saisie est inferieur au montant total
@login_required
def recherche_frais_repartition(request):
    frais_id = request.GET.get('frais')
    if not frais_id:
        return JsonResponse({'exists': False})
        
    try:
        # Récupérer le frais principal
        get_frais = Frais.objects.get(id=frais_id, ecole=request.user.ecole)
        
        # Calculer le total déjà réparti pour ce frais (pour l'année active de l'école)
        total = RepartitionFrais.objects.filter(
            frais=get_frais,
            ecole=request.user.ecole,
            annee__is_active=True,
            annee__ecole=request.user.ecole
        ).aggregate(Sum("montant"))["montant__sum"] or 0

        reste = get_frais.frais - total

        data = {
            'exists': True,
            'total': total,
            'reste': reste,
            'frais_global': get_frais.frais
        }
    except (Frais.DoesNotExist, ValueError):
        data = {'exists': False}
    return JsonResponse(data)

# la fonction qui verifier le montant que l'eleve doit payer par rapport a une tranche
@login_required
def recherche_montant_tranche(request):
    frais_id = request.GET.get('frais')
    get_eleve = request.GET.get('eleve')
    if not frais_id:
        return JsonResponse({'exists': False})  
    if not get_eleve:
        return JsonResponse({'exists': False})
        
    try:
        # Récupérer le frais deja paye par l'Eleve
        get_frais_paye = Paiement.objects.filter(frais=frais_id, eleve=get_eleve, ecole=request.user.ecole).aggregate(Sum("montant"))["montant__sum"] or 0
        
        # recupere le montant total du frais
        get_frais_total = RepartitionFrais.objects.get(id=frais_id, ecole=request.user.ecole).montant

        reste = get_frais_total - get_frais_paye

        data = {
            'exists': True,
            'total': get_frais_paye,
            'reste': reste
        }
    except (Paiement.DoesNotExist, ValueError):
        data = {'exists': False}
    return JsonResponse(data)

    
@login_required
def create_frais(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            data = request.POST
            get_id = data.get('id_frais')
            get_frais = data.get('frais_montant')
            get_classe = data.get('frais_classe')
            get_classe_by_id = Classes.objects.get(id = get_classe)
            

            # recuperer l'ecole, la section et l'annee
            ecole = request.user.ecole
            section = request.user.section
            annee = AnneeScolaires.objects.get(is_active=True)
            
            # verifier si l'id existe
            if get_id:
                get_frais_by_id = Frais.objects.get(id = get_id)
                get_frais_by_id.frais = get_frais
                get_frais_by_id.classe = get_classe_by_id
                get_frais_by_id.save()

                return JsonResponse({"success":True, "message": "Modifier avec succes"})
            else:
                # verifier si le frais existe
                if Frais.objects.filter(classe = get_classe_by_id, section = section, ecole = ecole, annee = annee).exists():
                    return JsonResponse({"success":False, "message": "le frais existe deja"})
                
                Frais.objects.create(
                    classe = get_classe_by_id,
                    frais = get_frais,
                    annee = annee,
                    section = section,
                    ecole = ecole
                )
                return JsonResponse({"success":True, "message": "enregistrer avec succes"})

@login_required
def create_repartition_frais(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            data = request.POST
            get_id = data.get('id_repartition')
            get_motif = data.get('repartition_motif')
            get_montant = data.get('repartition_montant')
            get_frais = data.get('repartition_frais')
            get_frais_id = Frais.objects.get(id = get_frais)

            # recuperer l'ecole, la section et l'annee
            ecole = request.user.ecole
            section = request.user.section
            annee = AnneeScolaires.objects.get(ecole = ecole, is_active=True)

            # verifier si l'id existe
            if get_id:
                get_id_rep = RepartitionFrais.objects.get(id = get_id)
                get_id_rep.motif = get_motif
                get_id_rep.frais = get_frais_id
                get_id_rep.montant = get_montant
                get_id_rep.save()

                # return redirect(reverse('setting') + '#repartition')
                return JsonResponse({"success":True, "message":"Modifier avec succes"})
            
            # verifier si le repartition existe
            if RepartitionFrais.objects.filter(motif = get_motif, frais = get_frais_id, section = section, ecole = ecole, annee = annee).exists():
                return JsonResponse({"success":False, "message": "Motif et frais deja enregistrer"})

            RepartitionFrais.objects.create(
                motif = get_motif,
                frais = get_frais_id,
                section = section,
                montant = get_montant,
                ecole = ecole,
                annee = annee
            )
            # return redirect(reverse('setting') + '#repartition')
            return JsonResponse({"success":True, "message":"enregistrer avec succes"})

@login_required
def comptabilitePage(request):
    if request.user.is_authenticated:
        ecole = request.user.ecole
        section = request.user.section
        eleves = Inscriptions.objects.filter(classe__section__ecole=ecole)
        return render(request, 'comptabilite/comptabilite.html', {'eleves': eleves})

# recherche un eleve
@login_required
def recherche_eleve(request):
    query = request.GET.get("q", "")
    if request.user.is_authenticated:
        if query:
            # recuperer l'eleve par rapport a son nom, prenom ou postnom tout en respectant la section et l'ecole
            ecole = request.user.ecole
            section = request.user.section
            # On passe par la table Inscriptions (qui lie Eleve, Classe, Section, Ecole)
            eleves = Eleves.objects.filter(
                Q(matricule__icontains=query) | Q(nom__icontains=query) | Q(prenom__icontains=query),
                inscriptions__classe__section=section,
                inscriptions__classe__section__ecole=ecole,
                inscriptions__annee__is_active=True
            ).distinct()[:10]
            data = []
            for eleve in eleves:
                data.append({
                    'id': eleve.id,
                    'nom': eleve.nom,
                    'prenom': eleve.prenom,
                    'postnom': eleve.postnom,
                })
            return JsonResponse(data, safe=False)

# recherche le frais pour la classe par rapport a l'eleve
@login_required
def recherche_frais_classe(request):
    get_eleve = request.GET.get("eleve_id")
    if not get_eleve:
        return JsonResponse({"exists": False, "message": "Aucun élève spécifié"})
        
    if request.user.is_authenticated:
        # recuperer l'ecole
        ecole = request.user.ecole
        # recuperer l'annee encours
        annee = AnneeScolaires.objects.get(is_active=True, ecole = ecole)
        # recuperer la section
        section = request.user.section
        # recuperer la classe dans inscription
        inscription = Inscriptions.objects.filter(eleve = get_eleve, annee = annee).first()
        if not inscription:
            return JsonResponse({"exists":False, "message": "L'eleve n'est pas inscrit"})
        classe = inscription.classe
        # recuperer les frais paye par l'eleve
        frais_paye = Paiement.objects.filter(eleve = get_eleve, annee = annee, ecole = ecole, section = section).aggregate(Sum("montant"))["montant__sum"] or 0
        
        try:
            # recuperer les frais
            frais = Frais.objects.get(classe = classe, section = section, ecole = ecole, annee = annee)
        except Frais.DoesNotExist:
            return JsonResponse({"exists": False, "message": "Aucun frais n'est configuré pour cette classe"})
            
        montant = 0
        if frais_paye:
            montant = frais_paye
        if montant == 0:
            montant = frais.frais
        data = {
            'exists': True,
            'montant': montant,
        }

        return JsonResponse(data, safe=False)

# enregistrement de paiement de frais scolaire
@login_required
def create_paiement(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            data = request.POST
            get_id = data.get('id_paiement')
            get_montant = data.get('montant')
            get_frais = data.get('frais')
            get_eleve = data.get('eleve')
            get_frais_id = RepartitionFrais.objects.get(id = get_frais)
            get_eleve_id = Eleves.objects.get(id = get_eleve)

            # recuperer l'ecole, la section, l'annee et l'utilisateur
            utilisateur = request.user.id
            ecole = request.user.ecole
            section = request.user.section
            annee = AnneeScolaires.objects.get(ecole = ecole, is_active=True)

            # verifier si l'eleve a deja paye le frais par rapport au frais selectionner
            get_montant_paye = Paiement.objects.filter(eleve = get_eleve_id, frais = get_frais_id, ecole = ecole, section = section, annee = annee).aggregate(Sum("montant"))["montant__sum"] or 0

            # si le montant est egale a 0 que les donnees considere comme nouveau paiement avec une nouvelle frais id
            
