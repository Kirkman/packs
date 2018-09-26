"""packs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from viewer import views


app_name = 'viewer'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # ex: /viewer/
    url(r'^$', views.index, name='index'),
    # ex: /viewer/group/blocktronics/
    url(r'group/(?P<group_slug>[\w-]+)/$', views.group, name='group'),
    # ex: /viewer/artist/kirkman
    url(r'artist/(?P<artist_slug>[\w-]+)/$', views.artist, name='artist'),
    # ex: /viewer/artist/blocktronics/blocktronics-6710
    url(r'pack/(?P<group_slug>[\w-]+)/(?P<pack_slug>[\w-]+)/$', views.pack, name='pack'),
    # ex: /viewer/blocktronics-6710/we-are-a-nation-of-immigrants/
    url(r'piece/(?P<pack_slug>[\w-]+)/(?P<piece_slug>[\w-]+)/$', views.piece, name='piece'),
]




