from django.db import models
from scolaireapp.models import Classes, AnneeAcademiques, Eleves

# Create your models here.

class Cours(models.Model):
    designation = models.CharField(max_length=50)
    classe = models.ForeignKey(Classes, on_delete=models.CASCADE)
    ponderation = models.IntegerField()
    is_active = models.BooleanField(default=True)

class Enseignants(models.Model):
    noms = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    sexe = models.CharField(max_length=50)
    datenaissance = models.DateField(auto_now=False)
    lieunaissance = models.CharField(max_length=50)
    grade = models.CharField(max_length=50)
    etatcivil = models.CharField(max_length=50)

class Affectations(models.Model):
    enseignant = models.ForeignKey(Enseignants, on_delete=models.CASCADE)
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE)
    annee = models.ForeignKey(AnneeAcademiques, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

class Ponderations(models.Model):
    point_obtenu = models.FloatField()
    eleve = models.ForeignKey(Eleves, on_delete=models.CASCADE)
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE)
    periode = models.CharField(max_length=50) 
    annee = models.ForeignKey(AnneeAcademiques, on_delete=models.CASCADE)



