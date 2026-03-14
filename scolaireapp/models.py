from django.db import models
from user.models import *
import uuid

# Create your models here.

class Parents(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    profession = models.CharField(max_length=50)
    email = models.CharField(max_length=50, null=True)
    adresse = models.CharField(max_length=50)
    telephone = models.IntegerField(unique=True)

class Eleves(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    matricule = models.CharField(max_length=50, null=True)
    nom = models.CharField(max_length=50)
    postnom = models.CharField(max_length=50, null=True)
    prenom = models.CharField(max_length=50)
    sexe = models.CharField(max_length=50)
    lieunaissance = models.CharField(max_length=50)
    datenaissance = models.DateField(auto_now_add=False)
    telephone = models.IntegerField()
    adresse = models.TextField()
    photo = models.ImageField(upload_to='eleves')
    parent = models.ForeignKey(Parents, on_delete=models.CASCADE)

class Options(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    option = models.CharField(max_length=50)
    ecole = models.ForeignKey(Ecole, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)

class Classes(models.Model): 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    classe = models.CharField(max_length=50)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True)
    ecole = models.ForeignKey(Ecole, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)

class AnneeScolaires(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    annee = models.CharField(max_length=50)
    ecole = models.ForeignKey(Ecole, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)

class Inscriptions(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    classe = models.ForeignKey(Classes, on_delete=models.CASCADE)
    eleve = models.ForeignKey(Eleves, on_delete=models.CASCADE)
    annee = models.ForeignKey(AnneeScolaires, on_delete=models.CASCADE)
    option = models.ForeignKey(Options, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    dateinscription = models.DateField(auto_now=True)




