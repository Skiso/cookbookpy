from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Avg
from django.shortcuts import render, redirect
from cookbook.forms import RecetteForm, InscriptionForm, NoteForm, RecetteImage, CommentaireForm
from cookbook.models import Recette, Note, Commentaire
from django.shortcuts import get_object_or_404
from datetime import datetime


# Create your views here.
def index(request):

    return redirect('afficher')


def afficher(request):
    recettes = Recette.objects.all();
    paginator = Paginator(recettes, 3)
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

def consulter(request, id):
    commentaire_formu = CommentaireForm(request.POST)
    recette = get_object_or_404(Recette, id=id)
    note = Note.objects.filter(recette=id).aggregate(Avg('note'))
    noted = 0
    if(request.user.is_authenticated()):
        noted = Note.objects.filter(recette=id, user=request.user).count()
    form_note = ''
    if noted == 0:
        form_note = NoteForm()

    commentaire = Commentaire.objects.filter(recette=recette)
    images = RecetteImage.objects.filter(recette=recette)

    paginator = Paginator(commentaire, 1)
    page = request.GET.get('page')
    try:
        commentaire = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        commentaire = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        commentaire = paginator.page(paginator.num_pages)

    contexte = {
        'recette': recette,
        'note': note,
        'commentaire': commentaire,
        'form_note': form_note,
        'form_comm': commentaire_formu,
        'images': images,
    }

    return render(request, 'cookbook/consulter.html', contexte)

@login_required
def modifier(request, id):
    recette = get_object_or_404(Recette, id=id)
    form = RecetteForm(instance=recette)
    if request.method == 'POST':
        form = RecetteForm(request.POST, request.FILES)
        if form.is_valid():
            recette.titre = form.cleaned_data['titre']
            recette.type = form.cleaned_data['type']
            recette.cout = form.cleaned_data['cout']
            recette.ingredients = form.cleaned_data['ingredients']
            recette.etape = form.cleaned_data['etape']
            recette.difficulte = form.cleaned_data['difficulte']
            recette.temps_prepa = form.cleaned_data['temps_prepa']
            recette.temps_cuisson = form.cleaned_data['temps_cuisson']
            recette.temps_repos = form.cleaned_data['temps_repos']
            recette.user = request.user
            recette.save()

            return redirect('mes_recettes')

    return render(request, "cookbook/modifier_recette.html", {
        'recette': recette,
        'form': form,
    })

@login_required
def mes_recettes(request):
    resultats = None;
    #Si user co
    if request.user.is_authenticated():
        resultats = Recette.objects.filter(user_id=request.user.id)
    contexte = {
        'resultats': resultats
    }
    return render(request, 'cookbook/mes_recettes.html', contexte)

@login_required
def supprimer(request, id):
    Recette.objects.get(id=id).delete()
    results = Recette.objects.filter(user_id=request.user.id)
    return redirect('mes_recettes')

@login_required
def noter(request,id):
    recette = get_object_or_404(Recette, id=id)
    if request.method == "POST":
        post = request.POST
        note = Note(
            note=post['note'],
            user=request.user,
            recette=recette
        )
        note.save()

        return redirect('consulter', id=id)

@login_required
def commenter(request,id):
    recette = get_object_or_404(Recette, id=id)
    if request.method == "POST":
        post = request.POST
        com = Commentaire(
            texte=post['libelle'],
            user=request.user,
            recette=recette,
            date=datetime.now()
        )
        com.save()

        return redirect('consulter', id=id)

@login_required
def rechercher(request):
    req = request.GET.get('chercher_req')
    critere = ''
    tri = ''
    if request.GET.get('critere') and request.GET.get('tri'):
        critere = request.GET.get('critere')
        tri = request.GET.get('tri')
        if tri == 'desc':
            resultats = Recette.objects.filter(titre__contains=req).order_by('-' + critere).select_related()
        elif tri == 'asc':
            resultats = Recette.objects.filter(titre__contains=req).order_by(critere).select_related()
    else:
        resultats = Recette.objects.filter(titre__contains=req).select_related()

    paginator = Paginator(resultats, 3)
    page = request.GET.get('page')
    try:
        resultats = paginator.page(page)
    except PageNotAnInteger:
        resultats = paginator.page(1)
    except EmptyPage:
        resultats = paginator.page(paginator.num_pages)

    contexte = {
        'page': page,
        'tri': tri,
        'critere': critere,
        'req': req,
        'resultats': resultats
    }

    return render(request, 'cookbook/resultat_recherche.html', contexte)