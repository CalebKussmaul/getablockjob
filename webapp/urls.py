from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signup/$', views.signup, name='home'),
    url(r'^game/$', views.game, name='game'),

    url(r'^gamedata.json$', views.gamedata, name='gamedata'),
    url(r'^delete_block/$', views.delete_block, name='game'),
    url(r'^get_board/$', views.get_board, name='game'),
    url(r'^place_block/$', views.place_block, name='game'),

]