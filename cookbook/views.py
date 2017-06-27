from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Avg
from django.shortcuts import render, redirect
from cookbook.forms import RecetteForm, InscriptionForm, NoteForm, RecetteImage, CommentaireForm
from cookbook.models import Recette, Note, Commentaire
from django.shortcuts import get_object_or_404


# Create your views here.
def index(request):

    return redirect('afficher')


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

@login_required
def ajouter(request):
    MainForm = RecetteForm()
    if request.method == 'POST':
        MainForm = RecetteForm(request.POST, request.FILES)
        if MainForm.is_valid():
            MainForm.instance.user = request.user
            MainForm.save()
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

@login_required
def consulter(request, id):
    recette = get_object_or_404(Recette, pk=id)
    commentaire_formu = CommentaireForm(request.POST)
    if (request.method == 'POST'):
        note_form = NoteForm(request.POST)
        if note_form.is_valid():
            note_form.recette = Recette.objects.get(recette=id)
            note_form.user = request.user
            note_form.save()
        if commentaire_formu.is_valid():
            commentaire_formu.id_recette = Recette.objects.get(id=id)
            commentaire_formu.user = request.user
            commentaire_formu.save()

    note = Note.objects.filter(recette=id).aggregate(Avg('note'))
    noted = 0
    if(request.user.is_authenticated()):
        noted = Note.objects.filter(recette=id, user=request.user).count()
    form_note = ''
    if noted == 0:
        form_note = NoteForm()

    commentaire = Commentaire.objects.filter(recette=recette)
    images = RecetteImage.objects.filter(recette=recette)

    contexte = {
        'recette': recette,
        'note': note,
        'commentaire': commentaire,
        'form_note': form_note,
        'form_comm': commentaire_formu,
        'images': images,
    }
    return render(request, 'cookbook/consulter.html', contexte)
