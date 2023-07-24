from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse

class CustomUser(AbstractUser):
    USER = (
        ('ADMIN', 'ADMIN'),
        ('STAFF', 'STAFF'),
        ('STUDENT', 'STUDENT'),
    )
    user_type = models.CharField(choices=USER, max_length=50, default='ADMIN')

#Annee scolaire
class Promotion(models.Model):
    annee_debut = models.CharField(max_length=100)
    annee_fin = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.annee_debut} - {self.annee_fin}"
 

# Il devrait avoir une relation manytomany avec le module
class Filiere(models.Model):
    nom = models.CharField(max_length=100)
    nom_abregee = models.CharField(max_length=100)
    date_cree = models.DateTimeField(auto_now_add=True)
    modules = models.ManyToManyField('Module', blank=True)
    date_modifie = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom
    
class Module(models.Model):
    nom = models.CharField(max_length=100)
    professeur = models.CharField(max_length=100)
    statut = models.CharField(
        choices=(
            ('en cours', 'en cours'),
            ('fini', 'fini'),
            ('commence', 'commence'),
            ('en attente', 'en attente'),
        ),
        max_length=10
    )
    date_debut = models.DateField(auto_now=True, blank=True) # just a datefield
    date_fini = models.DateField(auto_now=True, blank=True) # blank=True

    date_cree = models.DateTimeField(auto_now_add=True)
    date_modifie = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.nom} -- {self.professeur}'


class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    sexe = models.CharField(max_length=100)
    telephone_etudiant = models.IntegerField(null=True, blank=True)
    telephone_parent = models.IntegerField(null=True, blank=True)
    adresse = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='student_image', default='student_default_image.png')
    date_de_naissance = models.CharField(max_length=25, null=True, blank=True) # use charfield
    immatriculation = models.CharField(max_length=20)    
    classe = models.CharField(
        choices = (
            ('L1', 'Licence I'),
            ('L2', 'Licence II'),
            ('L3', 'Licence III'),
        ),
        max_length=15
    )
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)
    modules = models.ManyToManyField(Module, blank=True) 
    date_inscription = models.DateField(auto_now_add=True)
    date_dernier_modification = models.DateField(auto_now_add=True) # should appear some where on the admin and profile page

    def __str__(self):
        return f"{self.user.first_name}-{self.user.last_name}-{self.immatriculation}"
    

class Staff(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='staff_image', default='staff_default_image.png')
    adresse = models.TextField()
    sexe = models.CharField(max_length=100)
    modules = models.ManyToManyField(Module)  
    telephone = models.IntegerField()
    date_cree = models.DateTimeField(auto_now_add=True)
    date_modifie = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE) # No need of this
    surnom = models.CharField(max_length=20, null=True, blank=True) # This should be an optional field
    background_image = models.ImageField(upload_to='background_image', default='technosup_background_image.png', null=True, blank=True)
    description_profile = models.TextField(max_length=2000, help_text='Decrivez un peu de vous... votre personnalite, votre ambitions, etc', null=True, blank=True) #This should be an optional field


    def __str__(self):
        return f"{self.user.email}"


class StudentRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    modules = models.ForeignKey(Module, on_delete=models.CASCADE)
    note = models.FloatField(default=0)
    date_cree = models.DateTimeField(auto_now_add=True)
    date_modifie = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.student.user.first_name} - {self.note}'
    

class Message(models.Model):
    envoyeur = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    titre_message = models.CharField(max_length=100)
    message = models.TextField()
    destinataire_email = models.EmailField()
    date_cree = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.message[:100]
    


class Contact(models.Model):
    nom_prenom = models.TextField()
    email = models.EmailField()
    telephone = models.IntegerField()
    motive_message = models.TextField()

    def __str__(self):
        return f"{self.nom_prenom} -- {self.telephone}"