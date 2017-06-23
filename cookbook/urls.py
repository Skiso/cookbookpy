from django.conf.urls import url
from django.contrib import admin

from cookbook import views
from cookbook.views import afficher

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^afficher/$', afficher, name='afficher'),
    url(r'^connexion$', views.connexion, name='connexion'),
]