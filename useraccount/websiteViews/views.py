from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render

from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout

# Create your views here.
from rest_framework.authtoken.models import Token

import useraccount
from django.contrib.auth.forms import AuthenticationForm  # add this

from space.models import Space
from useraccount.forms.login_form import LoginForm
from useraccount.forms.register_form import RegistrationForm
from useraccount.models import ProfileModel, UserAccount


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


# def signup_view(request):
#     return render(request, 'Modified_files/sign-up.html',{"form":RegistrationForm()})


def register(request):
    # if request.method == 'POST':
    #     form = RegistrationForm(request.POST)
    #
    #     if form.is_valid():
    #         print("form is valid")
    #         user = UserAccount.objects.create_user(
    #             username=form.cleaned_data['email'],
    #
    #             email=form.cleaned_data['email'],
    #             password=form.cleaned_data['password'],
    #             first_name=form.cleaned_data['first_name'],
    #             last_name=form.cleaned_data['last_name'],
    #         )
    #         user.save()
    #         # messages.success(request, f'Account created for {form.cleaned_data["username"]}!')
    #         messages.success(request, 'Signup successful! You are now logged in.')  # Add success message
    #
    #         return redirect('login')
    #     else:
    return render(request, 'Modified_files/sign-up.html', {'form': RegistrationForm()})


# else:
#     form = RegistrationForm()

# return render(request, 'Modified_files/sign-up.html', {'form': form})


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
                Token.objects.get_or_create(user=user)

                messages.success(request, f'Hello {user.username}! You have been logged in')
                return redirect('/')  # Replace 'dashboard' with your desired URL for logged-in users
            else:
                messages.error(request, 'Email or password is incorrect.')
                return render(request, 'Modified_files/sign-in.html', {'form': form})

            # if user is not None:
            #     login(request, user)
            #     messages.success(request, f'Hello {user.username}! You have been logged in')
            # else:
            #     messages.error(request, 'Login failed!')
            # return redirect('/')  # Replace 'dashboard' with your desired URL for logged-in users

        # else:
        #     messages.error(request, 'Invalid login credentials.')
        #     return render(request, 'Modified_files/sign-in.html', {'form': form})


# render login form
def login_view(request):
    if request.method == 'POST':
        return login_user(request)
    else:
        if request.user.is_authenticated:
            return redirect('/')
        else:
            form = LoginForm(request.POST)
            return render(request, 'Modified_files/sign-in.html', {'form': form})

    # if request.user.is_authenticated:
    #     return redirect('/')
    # return render(request, 'Modified_files/sign-in.html')


def IndexView(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        profile = ProfileModel.objects.get(user=request.user.id)
        spaces = Space.objects.all()

        return render(request, 'Modified_files/index.html', {
            'user': request.user,
            'profile': profile,
            'spaces': spaces,
        })


def logout_view(request):
    logout(request)
    # messages.clear(request)

    messages.success(request, 'You have been logged out.')
    return redirect('login')
