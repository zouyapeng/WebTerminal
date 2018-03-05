# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import login

from models import UserProfile

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100,
                               label='Username',
                               widget=forms.TextInput(attrs={'class' : 'form-control',
                                                             'type': 'text',
                                                             'placeholder':'Username'}))
    password = forms.CharField(max_length=100,
                               label='Password',
                               widget=forms.PasswordInput(attrs={'class' : 'form-control',
                                                                 'type': 'password',
                                                                 'placeholder':'Password'}))

    remember_me = forms.BooleanField(required=False ,widget=forms.CheckboxInput(attrs={'type':'checkbox',
                                                                                    'value':'remember-me'}))


class ProfileForm(forms.Form):
    username = forms.CharField(max_length=100,
                               label='Username',
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'type': 'text',
                                                             'readonly': ''}))
    avatar = forms.ImageField(label='Avatar', required=False)

    def clean(self):
        super(ProfileForm, self).clean()
        upload_to = '/upload'
        if not 'avatar' in self.cleaned_data:
            return self.cleaned_data
        else:
            if self.cleaned_data['avatar'] is None:
                return None
            else:
                upload_to += self.cleaned_data['avatar'].name

    def save(self):
        form = self.cleaned_data
        user = User.objects.get(username= form['username'])
        userprofile = UserProfile.objects.get(user=user)

        if form['avatar'] is not None:
            userprofile.avatar = form['avatar']

        userprofile.save()