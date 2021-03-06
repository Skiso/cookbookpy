from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from cookbook import views
from cookbook.views import afficher, ajouter, inscription, consulter, modifier, supprimer, mes_recettes, noter,\
    commenter, rechercher

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^afficher/$', afficher, name='afficher'),
    url(r'^ajouter/$', ajouter, name='ajouter'),
    url(r'^mes_recettes/$', mes_recettes, name='mes_recettes'),
    url(r'^supprimer/(?P<id>\d+)/$', supprimer, name='supprimer'),
    url(r'^rechercher/$', rechercher, name='rechercher'),
    url(r'^consulter/(?P<id>\d+)/', consulter, name="consulter"),
    url(r'^noter/(?P<id>\d+)/', noter, name="noter"),
    url(r'^commenter/(?P<id>\d+)/', commenter, name="commenter"),
    url(r'^modifier/(?P<id>\d+)/', modifier, name="modifier"),
    url(r'^inscription/$', inscription, name='inscription'),
    url(r'^connexion/$', auth_views.login, name='connexion'),
    url(r'^deconnexion/$', auth_views.logout, {'next_page': '/cookbook/connexion/'}),

]