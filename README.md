Projet recette Master2

Utilisation d'une lib "https://github.com/Chive/django-multiupload"
pour le multiupload d'images

cmd : 
pip install django-multiupload
pip install Pillow

Models :
Recette(titre,type,difficulte,cout,temps_prepa,temps_cuisson,temps_repos,etape,ingredients,user)
FK : user

Commentaire(user,texte,date,recette)
FK : user

Note(user,note,recette)
FK : user, recette

Jeu de données :
dans /cookbook/fixtures/data.json
>> cmd python manage.py loaddata

