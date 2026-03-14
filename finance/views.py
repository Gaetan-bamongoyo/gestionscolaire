from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from scolaireapp.models import *
from .models import *
from django.urls import reverse
from django.db.models import Sum
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
        eleves = Eleve.objects.filter(classe__section__ecole=ecole)
        return render(request, 'comptabilite/comptabilite.html', {'eleves': eleves})
