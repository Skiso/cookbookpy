from django.conf.urls import url
from django.contrib import admin

from cookbook import views
from cookbook.views import afficher, connexion, ajouter

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^afficher/$', afficher, name='afficher'),
    url(r'^connexion$', connexion, name='connexion'),
    url(r'^ajouter/$', ajouter, name='ajouter'),
]