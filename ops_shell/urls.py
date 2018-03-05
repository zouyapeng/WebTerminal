"""ops_shell URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin

#Webterminal api
from rest_framework import routers
from shell.api import ServerGroupViewSet,ServerInforViewSet,CommandsSequenceViewSet,CredentialViewSet

from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy
from django.views.static import serve

#Register webterminal api
router = routers.DefaultRouter()
router.register('servergroup', ServerGroupViewSet)
router.register('serverinfo', ServerInforViewSet)
router.register('commandssequence', CommandsSequenceViewSet)
router.register('credential', CredentialViewSet)

from shell import urls as shell_urls
from account import urls as account_urls

from settings import MEDIA_ROOT

urlpatterns = [
    url(r'^$', RedirectView.as_view(url=reverse_lazy('shell:index')), name='index'),
    url(r'^shell/', include(shell_urls, namespace='shell')),
    url(r'^account/', include(account_urls, namespace='account')),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT})
]
