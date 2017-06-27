from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from cookbook import views
from cookbook.views import afficher, ajouter, inscription, consulter, modifier

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^afficher/$', afficher, name='afficher'),
    url(r'^ajouter/$', ajouter, name='ajouter'),
    url(r'^consulter/(?P<id>\d+)/', consulter, name="consulter"),
    url(r'^modifier/(?P<id>\d+)/', modifier, name="modifier"),
    url(r'^inscription/$', inscription, name='inscription'),
    url(r'^connexion/$', auth_views.login, name='connexion'),
    url(r'^deconnexion/$', auth_views.logout, name='deconnexion'),

]