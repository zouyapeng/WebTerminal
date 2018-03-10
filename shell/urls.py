from django.conf.urls import url

from shell.views import IndexView
from shell.views import ServerListView, SshTerminalKill, server_list_js

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^sshterminalkill/$',SshTerminalKill.as_view(), name='sshterminalkill'),
    url(r'^(?P<region>[\w-]+)/(?P<role>[\w-]+)/$', ServerListView.as_view(), name='server_list'),
    url(r'^(?P<region>[\w-]+)/(?P<role>[\w-]+)/js/$', server_list_js, name='server_list_js'),
]