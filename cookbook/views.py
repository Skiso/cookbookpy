from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from cookbook.forms import ConnexionForm, RecetteForm, EtapesForm, InscriptionForm
from cookbook.models import Recette


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

def ajouter(request):
    MainForm = RecetteForm()
    EtapeFormu = EtapesForm()
    if request.method == 'POST':
        MainForm = RecetteForm(request.POST)
        if MainForm.is_valid():
            recettes = MainForm.save()
            recettes.user = request.user
            recettes.save()
            EtapeFormu = EtapesForm(request.POST, instance=recettes)
            if EtapeFormu.is_valid():
                EtapeFormu.save()
            return render(request, "cookbook/nouvelle_recette.html", {
                'MainForm': MainForm,
                'EtapeForm': EtapeFormu,
                'create_success': 'success'
            })

    return render(request, "cookbook/nouvelle_recette.html", {
        'MainForm': MainForm,
        'EtapeForm': EtapeFormu,
    })

def inscription(request):
    if request.method == 'POST':
        user_form = InscriptionForm(request.POST)
        if user_form.is_valid():
            user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password1'])
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.save()
            contexte = {
                'form': AuthenticationForm,
                'success_message': 'success'
            }
            return render(request, 'cookbook/connexion.html', contexte)
    else:
        user_form = InscriptionForm()
    contexte = {
        'formulaire_user': user_form,
    }
    return render(request, 'cookbook/inscription.html', contexte)
