from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.

class Ecole(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=50)
    adresse = models.CharField(max_length=50)
    telephone = models.IntegerField()
    email = models.CharField(max_length=50, null=True)
    arreteministeriel = models.CharField(max_length=50)
    datecreation = models.DateField()
    dateajout = models.DateField(auto_now=True)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)

    class Meta:
        verbose_name = 'Ecole'
        verbose_name_plural = 'Ecoles'

class Section(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    section = models.CharField(max_length=50)
    ecole = models.ForeignKey(Ecole, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Section'
        verbose_name_plural = 'Sections'

class Utilisateurs(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=50, null=True)
    ecole = models.ForeignKey(Ecole, on_delete=models.CASCADE, null=True, blank=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True)
    photo = models.ImageField(upload_to='profiles/', null=True, blank=True)

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
