#create login form
import django.forms
from django import forms

import useraccount
from useraccount.models import UserAccount


#create login form
from django.contrib.auth.forms import AuthenticationForm, authenticate


class LoginForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = ['email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
