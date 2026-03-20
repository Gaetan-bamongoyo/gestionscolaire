from django.db import models
import uuid
from scolaireapp.models import *
from user.models import *


# Create your models here. 

class Frais(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    classe = models.ForeignKey(Classes, on_delete=models.CASCADE, blank=True, null=True)
    frais = models.IntegerField()
    annee = models.ForeignKey(AnneeScolaires, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    ecole = models.ForeignKey(Ecole, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Frais'
        verbose_name_plural = 'Frais'

class RepartitionFrais(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    motif = models.CharField(max_length=50)
    frais = models.ForeignKey(Frais, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    ecole = models.ForeignKey(Ecole, on_delete=models.CASCADE)
    annee = models.ForeignKey(AnneeScolaires, on_delete=models.CASCADE)
    montant = models.IntegerField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'RepartitionFrais'
        verbose_name_plural = 'RepartitionFrais'

class Paiement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    eleve = models.ForeignKey(Eleves, on_delete=models.CASCADE, blank=True, null=True)
    frais = models.ForeignKey(RepartitionFrais, on_delete=models.CASCADE, blank=True, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, blank=True, null=True)
    ecole = models.ForeignKey(Ecole, on_delete=models.CASCADE, blank=True, null=True)
    annee = models.ForeignKey(AnneeScolaires, on_delete=models.CASCADE, blank=True, null=True)
    montant = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Utilisateurs, on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Paiement'
        verbose_name_plural = 'Paiements'
        



    
