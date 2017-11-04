from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signup/$', views.signup, name='home'),
    url(r'^game/$', views.game, name='game'),
    url(r'^gamedata.json$', views.gamedata, name='gamedata'),

]