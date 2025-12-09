from django.db import models

# Create your models here.

class Parents(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    profession = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    adresse = models.CharField(max_length=50)
    telephone = models.IntegerField()

class Eleves(models.Model):
    # matricule = models.CharField(max_length=50)
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

class Niveaux(models.Model):
    niveau = models.CharField(max_length=50)

class Options(models.Model):
    option = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

class Classes(models.Model):
    classe = models.CharField(max_length=50)
    niveau = models.ForeignKey(Niveaux, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True) 

class AnneeAcademiques(models.Model):
    annee = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

class Inscriptions(models.Model):
    classe = models.ForeignKey(Classes, on_delete=models.CASCADE)
    eleve = models.ForeignKey(Eleves, on_delete=models.CASCADE)
    annee = models.ForeignKey(AnneeAcademiques, on_delete=models.CASCADE)
    option = models.ForeignKey(Options, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)
    dateinscription = models.DateField(auto_now=True)




