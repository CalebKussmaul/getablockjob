from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

    #url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),

urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'logged_out.html'}, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    #url(r'^login/$', views.login,  name='login'),
    #url(r'^login/$', views.logon, name='home'),
    url(r'^game/$', views.game, name='game'),

    url(r'^gamedata.json$', views.gamedata, name='gamedata'),
    url(r'^delete_block/$', views.delete_block, name='game'),
    url(r'^get_board/$', views.get_board, name='game'),
    url(r'^place_block/$', views.place_block, name='game'),

]
