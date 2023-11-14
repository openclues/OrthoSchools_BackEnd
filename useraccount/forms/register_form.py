from django import forms
from useraccount.models import UserAccount


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
