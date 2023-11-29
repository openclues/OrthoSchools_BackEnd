from django import forms
from useraccount.models import UserAccount


class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = UserAccount
        fields = ['email', 'password', 'first_name', 'last_name', "confirm_password"]
        widgets = {
            'password': forms.PasswordInput(),
            'confirm_password': forms.PasswordInput(),
        }
