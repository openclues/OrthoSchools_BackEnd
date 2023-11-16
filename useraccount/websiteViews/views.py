from django.contrib import messages
from django.shortcuts import render

from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout

# Create your views here.
import useraccount
from django.contrib.auth.forms import AuthenticationForm  # add this

from useraccount.forms.login_form import LoginForm
from useraccount.forms.register_form import RegistrationForm
from useraccount.models import ProfileModel


def signup_view(request):
    return render(request, 'Modified_files/sign-up.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')  # Replace 'success_url' with your desired URL
    else:
        form = RegistrationForm()

    return render(request, 'Modified_files/sign-up.html', {'form': form})


# render login form
def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    return render(request, 'Modified_files/sign-in.html')


def login_user(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                messages.success(request, f'Hello {user.username}! You have been logged in')
            else:
                messages.error(request, 'Login failed!')
            return redirect('/')  # Replace 'dashboard' with your desired URL for logged-in users

        else:
            messages.error(request, 'Invalid login credentials.')
            return render(request, 'Modified_files/sign-in.html', {'form': form})


def IndexView(request):
    if not request.user.is_authenticated:
        print("not request.user.is_authenticated")
        return redirect('login')
    else:

        profile = ProfileModel.objects.get_or_create(user=request.user)
        return render(request, 'Modified_files/index.html', {
            'user': request.user,
            'profile': profile
        })


def logout_view(request):
    logout(request)
    return redirect('login')
