from django import forms

from useraccount.models import ProfileModel


class ProfileAndUserForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(required=True)
    address = forms.CharField(max_length=100, required=False)
    phone = forms.CharField(max_length=100, required=False)
    bio = forms.CharField(max_length=100, required=False)
    cover = forms.ImageField(required=False)
    profileImage = forms.ImageField(required=False)
    place_of_work = forms.CharField(max_length=100, required=False)
    speciality = forms.CharField(max_length=100, required=False)
    study_in = forms.CharField(max_length=100, required=False)
    title = forms.CharField(max_length=100, required=False)
    selfie = forms.ImageField(required=False)


