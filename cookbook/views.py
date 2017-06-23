from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render
from cookbook.models import Recette, Ingredients, Liste_Ingredients, Etapes_Recette, Note, Commentaire

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def afficher(request):
    recettes = Recette.objects.all();
    typeObjet=None
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