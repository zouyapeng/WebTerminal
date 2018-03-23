from django.conf.urls import url

from shell.views import IndexView
from shell.views import ServerListView, SshTerminalKill, server_list_js
from shell.views import SshLogList, SshTerminalMonitor, SshLogPlay

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^sshlogslist/$', SshLogList.as_view(), name='sshlogslist'),
    url(r'^sshterminalkill/$',SshTerminalKill.as_view(), name='sshterminalkill'),
    url(r'^sshlogplay/(?P<pk>[0-9]+)/', SshLogPlay.as_view(), name='sshlogplay'),
    url(r'^sshterminalmonitor/(?P<pk>[0-9]+)/', SshTerminalMonitor.as_view(), name='sshterminalmonitor'),
    url(r'^(?P<region>[\w-]+)/(?P<role>[\w-]+)/$', ServerListView.as_view(), name='server_list'),
    url(r'^(?P<region>[\w-]+)/(?P<role>[\w-]+)/js/$', server_list_js, name='server_list_js'),



]