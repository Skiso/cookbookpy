from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render

from cookbook.forms import ConnexionForm, RecetteForm
from cookbook.models import Recette, Ingredients, Liste_Ingredients, Etapes_Recette, Note, Commentaire


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def afficher(request):
    recettes = Recette.objects.all();
    typeObjet = None
    paginator = Paginator(recettes, 10)
    page = request.GET.get('page')
    try:
        recettes = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        recettes = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        recettes = paginator.page(paginator.num_pages)
    contexte = {
        'typeObjet': typeObjet,
        'recettes': recettes,
    }
    return render(request, 'cookbook/afficher.html', contexte)


def connexion(request):
    error = False

    if request.method == "POST":

        form = ConnexionForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data["username"]

            password = form.cleaned_data["password"]

            user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes

            if user:  # Si l'objet renvoyé n'est pas None

                login(request, user)  # nous connectons l'utilisateur

            else:  # sinon une erreur sera affichée

                error = True

    else:

        form = ConnexionForm()

    return render(request, 'cookbook/connexion.html', locals())


def ajouter(request):
    MainForm = RecetteForm()

    if request.method == 'POST':
        MainForm = RecetteForm(request.POST)
        if MainForm.is_valid():
            recettes = MainForm.save()
            recettes.user = request.user

            return render(request, "cookbook/nouvelle_recette.html", {
                'MainForm': MainForm,

                'create_success': 'success'
            })


    return render(request, "cookbook/nouvelle_recette.html", {
        'MainForm': MainForm,

    })
