from django.urls import path, re_path
from django.http import Http404
from . import views

def favicon_view(request):
    raise Http404

urlpatterns = [
    path('', views.m_index, name='m_index'),
    path('favicon.ico', favicon_view),
    path('keywords', views.m_getkeywords, name='m_getKeywords'),
    path('downloadArr', views.m_downloadArr, name='m_downloadArr'),
    re_path(r'^download/(?P<pdf>\d+-\d+)$', views.m_download, name='m_download'),
    path('login', views.m_login, name='m_login'),
    path('admin', views.m_admin, name='m_admin'),
    re_path(r'^(?P<pdf>\d+-\d+)$', views.m_index, name='m_index')
]