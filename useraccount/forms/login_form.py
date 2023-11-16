#create login form
import django.forms
from django import forms

import useraccount
from useraccount.models import UserAccount


#create login form
from django.contrib.auth.forms import AuthenticationForm, authenticate


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
