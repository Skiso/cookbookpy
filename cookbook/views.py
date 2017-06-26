from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Avg
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from cookbook.forms import ConnexionForm, RecetteForm, InscriptionForm, NoteForm
from cookbook.models import Recette, Note


# Create your views here.
def index(request):
    return render(request, 'cookbook/index.html')


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
    if request.method == 'POST':
        MainForm = RecetteForm(request.POST)
        if MainForm.is_valid():
            recettes = MainForm.save()
            recettes.user = request.user
            recettes.save()
            return redirect('afficher')

    return render(request, "cookbook/nouvelle_recette.html", {
        'MainForm': MainForm,
    })

def inscription(request):
    if request.method == 'POST':
        user_form = InscriptionForm(request.POST)
        if user_form.is_valid():
            user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password1'])
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.save()
            login(request, user)
            return redirect('afficher')
    else:
        user_form = InscriptionForm()
    contexte = {
        'formulaire_user': user_form,
    }
    return render(request, 'cookbook/inscription.html', contexte)

def consulter(request, id):

    if (request.method == 'POST'):
        note_form = NoteForm(request.POST)


        if note_form.is_valid():
            note = note_form.save()
            note.id_recette = Recette.objects.get(id=id)
            note.user = request.user
            note.save()


    recette = Recette.objects.get(id=id)
    note = Note.objects.filter(id_recette=id).aggregate(Avg('valeur'))
    noted = 0
    if(request.user.is_authenticated()):
        noted = Note.objects.filter(id_recette=id, user=request.user).count()
    form_note = ''
    if noted == 0:
        form_note = NoteForm();

    contexte = {
        'recette'    : recette,
        'notes'     : note,
        'form_note': form_note,

    }
    return render(request, 'cookbook/consulter.html', contexte)