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
    if request.user.is_authenticated == True:
        return redirect('/')
    return render(request, 'Modified_files/sign-in.html')


def login_user(request):
    if request.user.is_authenticated:
        return redirect('/')
    else :

        if request.method == 'POST':
            print("request.method == 'POST'")
            post = request.POST.copy()
            post['username'] = request.POST['email']
            request.POST = post
            print(request.POST['email'])
            print(request.POST['password'])
            print(request.POST['username'])

            form = AuthenticationForm(data = request.POST)
            print(form)
            if form.is_valid():
                return redirect('/')  # Replace 'dashboard' with your desired URL for logged-in users

            else:
                print("form.is_not_valid()")
                render(request, 'Modified_files/sign-in.html', {'form': form})
        else:
            print("request.method != 'POST'")
            form = LoginForm()  # Use your LoginForm for rendering the login form

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
        } )



def logout_view(request):
    logout(request)
    return redirect('login')