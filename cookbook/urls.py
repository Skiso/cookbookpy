from django.conf.urls import url
from django.contrib import admin

from cookbook import views
from cookbook.views import afficher, ajouter, inscription, consulter

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^afficher/$', afficher, name='afficher'),
    url(r'^ajouter/$', ajouter, name='ajouter'),
    url(r'^inscription/$', inscription, name='inscription'),
    url(r'^consulter/(?P<id>\d+)/', consulter, name="consulter"),
]