from django import forms
from django.forms import inlineformset_factory

from cookbook.models import Recette, Liste_Ingredients, Etapes_Recette


class ConnexionForm(forms.Form):

    username = forms.CharField(label="Nom d'utilisateur", max_length=30)

    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)

class RecetteForm(forms.ModelForm):
    required_css_class = 'required'
    class Meta:
        model = Recette
        fields = ['titre', 'type', 'difficulte', 'cout', 'temps_prepa', 'temps_cuisson', 'temps_repos']

class EtapesForm(forms.ModelForm):
    required_css_class = 'required'
    class Meta:
        model = Etapes_Recette
        fields = '__all__'

EtapeFormset = inlineformset_factory(Recette, Etapes_Recette, form=EtapesForm, can_delete=False)
