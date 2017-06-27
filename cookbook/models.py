from django.db import models
from django.contrib.auth.models import User

class Recette(models.Model):
    TYPES = (
        ('E', "Entrée"),
        ('P', "Plat principal"),
        ('D', "Dessert"),
    )

    DIFFICULTE = (
        ('1', "Simple"),
        ('2', "Moyen"),
        ('3', "Difficile"),
    )

    # Champs
    titre = models.CharField(max_length=200, verbose_name="titre")
    type = models.CharField(max_length=1,choices=TYPES, verbose_name="type de plat")
    difficulte = models.CharField(blank=True, max_length=1, choices=DIFFICULTE, verbose_name="difficulte")
    cout = models.IntegerField(blank=True, verbose_name="Coût de la recette")
    temps_prepa = models.IntegerField(blank=True, null=True, verbose_name="temps de préparation")
    temps_cuisson = models.IntegerField(blank=True, null=True, verbose_name="temps de cuisson")
    temps_repos = models.IntegerField(blank=True, null=True, verbose_name="temps de repos")
    etape = models.TextField(null=True, verbose_name="Etape de la recette")
    ingredients = models.TextField(null=True, verbose_name="Ingrédients de la recette")
    valide = models.BooleanField(default=False, verbose_name="validé ?")
    user = models.ForeignKey(User, default=False, on_delete=models.CASCADE, related_name="id_user")


    def __str__(self):
        return self.titre

class Commentaire(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentaire_user")
    texte = models.TextField(default=True, verbose_name="Texte")
    date = models.DateField(auto_now_add=True, verbose_name="date du commentaire")
    recette = models.ForeignKey(Recette, on_delete=models.CASCADE, related_name="commentaire_recette")


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="note_user")
    note = models.IntegerField(verbose_name="Note de la recette")
    recette = models.ForeignKey(Recette, on_delete=models.CASCADE, related_name="note_recette")

class RecetteImage(models.Model):
    recette = models.ForeignKey(Recette, verbose_name='recette')
    file = models.ImageField('Image', upload_to='images')