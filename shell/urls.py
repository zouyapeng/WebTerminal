from django.conf.urls import url

from shell.views import IndexView
from shell.views import ServerListView

urlpatterns = [
    url(r'^$',IndexView.as_view(), name='index'),
    url(r'^(?P<region>[\w-]+)/(?P<role>[\w-]+)/$', ServerListView.as_view(), name='server_list'),
]