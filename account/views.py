# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.encoding import force_text
from django.views.generic import FormView, RedirectView, TemplateView, ListView, DetailView
from forms import LoginForm, ProfileForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.shortcuts import HttpResponseRedirect

from models import UserProfile


# Create your views here.
class LoginView(FormView):
    form_class = LoginForm
    template_name = 'account/login.html'
    success_url = reverse_lazy("shell:index")

    def post(self, request, *args, **kwargs):
        # redirect_to = request.GET['next']
        form = self.get_form()
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data['remember_me']
            user = authenticate(username = username, password = password)
            if user:
                login(self.request, user)
                if not remember_me:
                    request.session.set_expiry(0)
            else:
                errors = form._errors.setdefault("password", ErrorList())
                errors.append(u"username or password is incorrect!")
                return self.render_to_response(self.get_context_data(form=form))

            # if redirect_to:
            #     return HttpResponseRedirect(redirect_to)
            return self.form_valid(form)
            # return HttpResponseRedirect(force_text(reverse_lazy('blog:index')))
        else:
            return self.form_invalid(form)


class LogoutView(RedirectView):
    permanent = True
    url = reverse_lazy("account:login")

    def post(self, request, *args, **kwargs):
        """Logout may be done via POST."""
        return self.get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect('/shell')


class Profile(FormView):
    login_required = True
    form_class = ProfileForm
    template_name = 'account/user_profile.html'
    success_url = reverse_lazy("account:profile")
    # success_url = reverse_lazy("blog:index")

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


    def get(self, request, *args, **kwargs):
        user = User.objects.get(username = request.user.username)
        self.initial = {
            'username': request.user.username,
            'avatar': user.user_profile.avatar,
        }

        return super(Profile, self).get(request, *args, **kwargs)