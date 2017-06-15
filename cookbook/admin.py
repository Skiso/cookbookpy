from django.contrib import admin
from cookbook.models import Recette, Commentaire, Etapes_Recette, Liste_Ingredients, Ingredients, Note

admin.site.register(Recette)
admin.site.register(Commentaire)
admin.site.register(Etapes_Recette)
admin.site.register(Liste_Ingredients)
admin.site.register(Ingredients)
admin.site.register(Note)



