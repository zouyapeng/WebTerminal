from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from views import LoginView, Profile, LogoutView

from django.contrib.auth.views import logout

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^profile/$', Profile.as_view(), name='profile')
]