from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from multiupload.fields import MultiFileField

from cookbook.models import Recette, Note, RecetteImage, Commentaire


class ConnexionForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)

class RecetteForm(forms.ModelForm):
    required_css_class = 'required'
    class Meta:
        model = Recette
        fields = ['titre', 'type', 'difficulte', 'cout', 'temps_prepa', 'temps_cuisson', 'temps_repos','ingredients','etape']

    files = MultiFileField(min_num=1, max_num=3, max_file_size=1024 * 1024 * 5)
    def save(self, commit=True):
         instance = super(RecetteForm, self).save(commit)
         for each in self.cleaned_data['files']:
             RecetteImage.objects.create(file=each, recette=instance)

         return instance


class InscriptionForm(UserCreationForm):
    required_css_class = 'required'
    last_name = forms.CharField(required=True, label="Nom")
    first_name = forms.CharField(required=True, label="Prenom")
    email = forms.EmailField(required= True, label="Email")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        def save(self, commit=True):
            user = super(InscriptionForm, self).save(commit=False)
            user.nom = self.cleaned_data['last_name']
            user.prenom = self.cleaned_data['first_name']
            user.email = self.cleaned_data['email']

            if commit:
                user.save()
            return user

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['note']

class CommentaireForm(forms.ModelForm):
    libelle = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 4}))
    class Meta:
        model = Commentaire
        fields = ['libelle']